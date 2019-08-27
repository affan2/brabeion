# from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model


class PlayerStat(models.Model):
    user = models.OneToOneField(get_user_model(), related_name="stats", on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
