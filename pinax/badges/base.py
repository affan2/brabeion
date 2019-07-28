from .models import BadgeAward
from .signals import badge_awarded

from django.conf import settings


def abstract_property(name):
    def attr(*args):
        msg = "attribute %r must be defined on child class." % name
        raise NotImplementedError(msg)

    return property(attr, attr)


class BadgeAwarded(object):
    def __init__(self, level=None, user=None, points_at=0):
        self.level = level
        self.user = user
        self.points_at = points_at


class BadgeDetail(object):
    def __init__(self, name=None, description=None, **kwargs):
        self.name = name
        self.description = description

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return str(self.name)


class Badge(object):
    async_ = False
    multiple = abstract_property("multiple")
    levels = abstract_property("levels")
    events = abstract_property("events")
    slug = abstract_property("slug")

    def award(self, **state):
        raise NotImplementedError("must be implemented on base class")

    def __init__(self):
        assert not (self.multiple and len(self.levels) > 1)
        for i, level in enumerate(self.levels):
            if not isinstance(level, BadgeDetail):
                self.levels[i] = BadgeDetail(level)

    def possibly_award(self, **state):
        """
        Will see if the user should be awarded a badge.  If this badge is
        asynchronous it just queues up the badge awarding.
        """
        assert "user" in state
        if self.async_:
            from .tasks import AsyncBadgeAward
            state = self.freeze(**state)
            AsyncBadgeAward.delay(self, state)
            return
        self.actually_possibly_award(**state)

    def actually_possibly_award(self, **state):
        """
        Does the actual work of possibly awarding a badge.
        """
        user = state["user"]
        force_timestamp = state.pop("force_timestamp", None)
        awarded = self.award(**state)
        if awarded is None:
            return
        if awarded.level is None:
            assert len(self.levels) == 1
            awarded.level = 1
        # awarded levels are 1 indexed, for convenience
        awarded = awarded.level - 1
        assert awarded < len(self.levels)
        if (
                not self.multiple and
                BadgeAward.objects.filter(user=user, slug=self.slug, level=awarded, site_id=settings.SITE_ID,)
        ):
            return
        extra_kwargs = {}
        if force_timestamp is not None:
            extra_kwargs["awarded_at"] = force_timestamp
        badge = BadgeAward.objects.create(
            user=user,
            slug=self.slug,
            level=awarded,
            points_at=awarded.points_at,
            site_id=settings.SITE_ID,
            **extra_kwargs
        )
        self.send_badge_messages(badge)
        badge_awarded.send(sender=self, badge_award=badge)

    def send_badge_messages(self, badge_award):
        """
        If the Badge class defines a message, send it to the user who was just
        awarded the badge.
        """
        user_message = getattr(badge_award.badge, "user_message", None)
        if callable(user_message):
            message = user_message(badge_award)
        else:
            message = user_message
        if message is not None:
            badge_award.user.message_set.create(message=message)

    def freeze(self, **state):
        return state


# Patch badge so badge.async is still available as an attribute on older Python
# versions.
setattr(Badge, "async", property(
    fget=lambda self: self.async_,
    fset=lambda self, value: setattr(self, "async_", value)))
