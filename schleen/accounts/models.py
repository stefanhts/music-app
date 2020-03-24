from django.db import models
from django.contrib.auth.models import User


class Friend(models.Model):
    name = models.CharField(max_length=20, unique=True)
    desc = models.CharField(max_length=80)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friend_of'
    )
