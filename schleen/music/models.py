from django.db import models
from django.contrib.auth.models import User
from enum import Enum
from django.utils import timezone


class Artist(models.Model):
    # create artist model
    name = models.CharField(max_length=50, unique=True)

    def get_name(self):
        return self.name


class Album(models.Model):
    # create album model
    name = models.CharField(max_length=80)

    artist = models.ForeignKey(
        'Artist',
        on_delete=models.CASCADE,
        null=True
    )

    def get_name(self):
        return self.name

    def get_artist(self):
        return self.artist

    class Meta:
        # disallow song artist repeats
        unique_together = [
            'artist',
            'name'
        ]


class Songs_list(models.Model):
    # create songs_list model which  is linked to users who created them
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_by',
        null=True
    )

    name = models.CharField(max_length=100)

    def get_name(self):
        return self.name


class Song(models.Model):
    # create song model which links to album, artist, songs_list
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

    def get_name(self):
        return self.name

    def get_artist(self):
        return self.artist

    def get_album(self):
        return self.album

    class Meta:
        # disallow song-artist-combo repeats
        unique_together = [
            'artist',
            'name',
            'album'
        ]


class Reviews(models.Model):
    Al = 'al'
    Ar = 'ar'
    So = 'so'
    Pl = 'pl'

    REVIEW_TYPE_OPTIONS = (
        (Al, 'AL'),
        (Ar, 'AR'),
        (So, 'SO'),
        (Pl, 'PL'),
    )

    review_type = models.CharField(
        max_length=2,
        choices=REVIEW_TYPE_OPTIONS,
        default=Al,
    )

    name = models.CharField(max_length=80)

    text = models.TextField()

    date = models.DateField()

    rating = models.FloatField()

    score = models.IntegerField()

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='written_by'
    )

    def get_name(self):
        return self.name

    def get_text(self):
        return self.text

    def get_date(self):
        return self.date

    def get_rating(self):
        return self.rating

    def get_score(self):
        return self.score

    def get_username(self):
        return self.user.username


class Album_Reviews(models.Model):
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
    )

    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
    )

    def get_review(self):
        return self.review

    def get_album(self):
        return self.album

    class Meta:
        unique_together = [
            'album',
            'review'
        ]


class Artist_Reviews(models.Model):
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
    )

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
    )

    def get_review(self):
        return self.review

    def get_artist(self):
        return self.artist

    class Meta:
        unique_together = [
            'artist',
            'review'
        ]


class Song_Reviews(models.Model):
    review = models.ForeignKey(
        Reviews,
        on_delete=models.CASCADE,
    )

    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
    )

    def get_review(self):
        return self.review

    def get_album(self):
        return self.song

    class Meta:
        unique_together = [
            'song',
            'review'
        ]

# class Playlist_Reviews(models.Model):
#     review = models.ForeignKey(
#         Reviews,
#         on_delete=models.CASCADE,
#     )
#
#     playlist = models.ForeignKey(
#         Songs_list,
#         on_delete=models.CASCADE,
#     )
