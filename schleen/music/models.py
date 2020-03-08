from django.db import models

class User(models.Model):
    usr_username = models.CharField(max_length=100)
    usr_desc = models.TextField()
    # cust_songs = [models.CharField(max_length=100)]
    # cust_albums = [models.CharField(max_length=100)]
    usr_img = models.ImageField(upload_to='pics')



class Song(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    date = models.DateField()


class SongList(models.Model):
    list = [Song]