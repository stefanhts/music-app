from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Artist(models.Model):
    #create artist model
    name = models.CharField(max_length=50, unique=True)


class Album(models.Model):
    #create album model
    name = models.CharField(max_length=80)

    artist = models.ForeignKey(
        'Artist',
        on_delete=models.CASCADE,
        null=True
    )


    class Meta:
        #disallow song artist repeats
        unique_together=[
            'artist',
            'name'
        ]


class Songs_list(models.Model):
    #create songs_list model which  is linked to users who created them
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_by',
        null=True
    )

    name = models.CharField(max_length=100)

class Song(models.Model):
    #create song model which links to album, artist, songs_list
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
        Songs_list,
        related_name='song'
    )

    class Meta:
        #disallow song-artist-combo repeats
        unique_together=[
            'artist',
            'name',
            'album'
        ]








