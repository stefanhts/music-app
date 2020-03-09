from django.shortcuts import render, redirect
from .models import Song, Songs, Artist, Album
from django.contrib import messages
import datetime

#TODO disalow empty fields and duplicate songs

def home(request):
    return render(request, 'home.html')


def user(request):

    lists = Songs.objects.filter(user=request.user, name='top 5').order_by('-id')[:5][::-1]

    list = []
    for e in lists:
        list.append(song_obj(Song.objects.filter(id=e.id).first().name,Song.objects.filter(id=e.id).first().artist.name))

    return render(request, 'user.html',{ 'list':list })


def topsongs(request):
#TODO This should be generalized for creating any type of list. We don't want duplicate songs in our db
    if request.method == 'POST':

        artists = [
            request.POST['artist1'],
            request.POST['artist2'],
            request.POST['artist3'],
            request.POST['artist4'],
            request.POST['artist5']
        ]

        songnames = [
            request.POST['song1'],
            request.POST['song2'],
            request.POST['song3'],
            request.POST['song4'],
            request.POST['song5']
        ]

        #TODO get this from spotify
        cur_alb ='TBD'

        #TODO generalize this
        list = 'top 5'

        for i in range(len(artists)):
            cur_art = artists[i]
            cur_song = songnames[i]
            artist = Artist.objects.create(name=cur_art)
            artist.save()
            album = Album.objects.create(name=cur_alb, artist=artist)
            album.save()
            song = Song.objects.create(name=cur_song, album=album, artist=artist)
            song.save()
            songs= Songs.objects.create(user=request.user, name=list)
            songs.song.add(song)
            songs.save()

        #TODO don't add duplicates, and replace if they are on the same list

            # if not Song.objects.filter(artist=cur_art, name=cur_song).exists():
            #     if not Album.objects.filter(name=cur_alb).exitsts():
            #         if not Artist.objects.filter(name=cur_art).exists():
            #             artist = Artist.objects.create(artist=cur_art)
            #             artist.save()
            #         else:
            #             artist = Artist.objects.get(name=cur_art)
            #         album = Album.objects.create(name=album, artist=artist)
            #         album.save()
            #     else:
            #         album = Album.objects.get(name=album, artist=artist)
            #     song = Song.objects.create(name=cur_song, album=album, artist=artist)
            #     song.save()
            # else:
            #     song = Song.objects.get(name=song, artist=artist, album=album)
            # if not Songs.objects.filter(User=request.user, name=list, song=song).exists():
            #     songs = Songs.objects.create(user=request.user, song=song, name=list)
            #     songs.save()
            # else:
            #     messages.info(request, 'duplicate or invalid song:',song.title)
            #     return redirect('topsongs')

        return redirect('/user')

    else:
        return render(request,'topsongs.html')


class song_obj:
    title = str
    artist = str

    def __init__(self,title,artist):
        self.title=title
        self.artist=artist