from django.db import models
from django.contrib.sites.models import Site

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model

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

    def __str__(self):
        return '%s (%s) awarded to %s' % (self.slug, self.level, self.user)

    def __getattr__(self, attr):
        return getattr(self._badge, attr)

    @property
    def badge(self):
        return self

    @property
    def _badge(self):
        from .registry import badges
        return badges._registry[self.slug]

    @property
    def name(self):
        return self._badge.levels[self.level].name

    @property
    def description(self):
        return self._badge.levels[self.level].description

    @property
    def image(self):
        image = self._badge.levels[self.level].image
        if image != '':
            return '%sbadges/128/%s' % (settings.STATIC_URL, self._badge.levels[self.level - 1].image)

        return False

    @property
    def points(self):
        return self._badge.levels[self.level].points

    @property
    def points_next(self):
        return self._badge.levels[self.level].points_next

    @property
    def required_badges(self):
        return self._badge.levels[self.level].required_badges

    @property
    def progress(self):
        return self._badge.progress(self.user, self.level)
