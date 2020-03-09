from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Artist(models.Model):
    name = models.CharField(max_length=50)


class Album(models.Model):
    name = models.CharField(max_length=80)

    artist = models.ForeignKey(
        'Artist',
        on_delete=models.CASCADE,
        null=True
    )

class Songs(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_by',
        null=True
    )

    name = models.CharField(max_length=100)

class Song(models.Model):
    name = models.CharField(max_length=100)

    artist = models.ForeignKey(
        'Artist',
        on_delete=models.CASCADE,
        related_name='artist',
        null=True
    )

    album = models.ForeignKey(
        'Album',
        on_delete=models.CASCADE,
        related_name='album',
        null=True
    )

    songs = models.ManyToManyField(
        Songs,
        related_name='song'
    )








