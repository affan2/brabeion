from django.db import models
from django.contrib.sites.models import Site

from django.conf import settings

from django.utils import timezone

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class BadgeAward(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, related_name="badges_earned", on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(default=timezone.now)
    slug = models.CharField(max_length=255)
    level = models.IntegerField()
    points_at = models.IntegerField(default=0)
    site = models.ForeignKey(Site, default=settings.SITE_ID,
                             verbose_name='site', on_delete=models.CASCADE)

    class Meta:
        db_table = 'brabeion_badgeaward'

    def __str__(self):
        return '%s (%s) awarded to %s' % (self.slug, self.level, self.user)

    def __getattr__(self, attr):
        return getattr(self._badge, attr) if self._badge is not None else None

    @property
    def badge(self):
        return self

    @property
    def _badge(self):
        from .registry import badges
        return badges._registry[self.slug] if self.slug in badges._registry else None

    @property
    def name(self):
        return self._badge.levels[self.level].name

    @property
    def description(self):
        return self._badge.levels[self.level].description if self._badge is not None else None

    @property
    def image(self):
        if self._badge is None:
            return False
        image = self._badge.levels[self.level].image
        if image != '':
            return '%sbadges/128/%s' % (settings.STATIC_URL, self._badge.levels[self.level - 1].image)

        return False

    @property
    def points(self):
        return self._badge.levels[self.level].points if self._badge is not None else None

    @property
    def points_next(self):
        return self._badge.levels[self.level].points_next if self._badge is not None else None

    @property
    def required_badges(self):
        return self._badge.levels[self.level].required_badges if self._badge is not None else None

    @property
    def progress(self):
        return self._badge.progress(self.user, self.level) if self._badge is not None else None
