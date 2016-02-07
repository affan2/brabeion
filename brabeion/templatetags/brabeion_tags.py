from django import template
from django.utils.translation import ugettext_lazy as _

from ..models import BadgeAward
from brabeion import badges


register = template.Library()


class BadgeCountNode(template.Node):
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) == 2:
            return cls(bits[1])
        elif len(bits) == 4:
            if bits[2] != "as":
                raise template.TemplateSyntaxError("Second argument to %r must "
                    "be 'as'" % bits[0])
            return cls(bits[1], bits[3])
        raise template.TemplateSyntaxError("%r takes either 1 or 3 arguments." % bits[0])

    def __init__(self, user, context_var=None):
        self.user = template.Variable(user)
        self.context_var = context_var

    def render(self, context):
        user = self.user.resolve(context)
        badge_count = BadgeAward.objects.filter(user=user).count()
        if self.context_var is not None:
            context[self.context_var] = badge_count
            return ""
        return unicode(badge_count)

@register.tag
def badge_count(parser, token):
    """
    Returns badge count for a user, valid usage is::

        {% badge_count user %}

    or

        {% badge_count user as badges %}
    """
    return BadgeCountNode.handle_token(parser, token)


class BadgesForUserNode(template.Node):
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) != 5:
            raise template.TemplateSyntaxError("%r takes exactly 4 arguments." % bits[0])
        if not (bits[2][0] in ('"', "'") and bits[2][-1] == bits[2][0]):
            raise template.TemplateSyntaxError("%r expects 2nd argument format to be '\"string\"'" % bits[0])
        if bits[3] != "as":
            raise template.TemplateSyntaxError("The 3rd argument to %r should "
                                               "be 'as'" % bits[0])
        return cls(bits[1], bits[2][1:-1], bits[4])

    def __init__(self, user, slug, context_var):
        self.user = template.Variable(user)
        self.slug = slug
        self.context_var = context_var

    def render(self, context):
        user = self.user.resolve(context)
        slug = self.slug

        filters = {'user': user}
        excludes = {}
        order_by = "-awarded_at"
        if not slug == '':
            if slug.startswith('not_'):
                excludes.update({'slug': slug.replace('not_', '')})
            else:
                filters.update({'slug': slug})
                order_by = "-level"
        context[self.context_var] = BadgeAward.objects.filter(**filters).exclude(**excludes).order_by(order_by )
        return ""


@register.tag
def badges_for_user(parser, token):
    """
    Sets the badges for a given user to a context var.  Usage:

        {% badges_for_user user slug as badges %}
    """
    return BadgesForUserNode.handle_token(parser, token)


class RequiredBadgesForUserLevelUpNode(template.Node):
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) != 5:
            raise template.TemplateSyntaxError("%r takes exactly 4 arguments." % bits[0])
        if bits[3] != "as":
            raise template.TemplateSyntaxError("The 3nd argument to %r should "
                                               "be 'as'" % bits[0])
        return cls(bits[1], bits[2], bits[3])

    def __init__(self, user, badge, context_var):
        self.user = template.Variable(user)
        self.badge = template.Variable(badge)
        self.context_var = context_var

    def render(self, context):
        user = self.user.resolve(context)
        level = self.badge.resolve(context)
        next_level = badges._registry[level.slug].levels[level.level]

        return_val = '0 points'
        for required_badge in next_level.required_badges:
            filters = {'user': user, 'slug': required_badge[0], 'level': required_badge[1]}
            try:
                BadgeAward.objects.get(**filters)
            except BadgeAward.DoesNotExist:
                #TODO: standardise indexes
                # decrement to get the NEXT levels require badge because 0-indexed 1-indexed
                return_val = _('%s badge required') % badges._registry[required_badge[0]].levels[required_badge[1] - 1]
            except BadgeAward.MultipleObjectsReturned:
                pass

        return return_val

@register.tag
def required_badges_for_user_levelup(parser, token):
    """
    Sets the badges for a given user to a context var.  Usage:

        {% required_badges_for_user_levelup user badge_to_check as badges %}
    """
    return RequiredBadgesForUserLevelUpNode.handle_token(parser, token)
