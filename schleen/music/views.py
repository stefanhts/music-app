from django.shortcuts import render, redirect
from .models import Song, Songs_list, Artist, Album, Reviews, Album_Reviews, Artist_Reviews, Song_Reviews
from django.db import IntegrityError
from django.contrib import messages
from enum import Enum
from datetime import date

# TODO disalow empty fields and duplicate songs

ERROR_MESSAGE = 'Uh oh, something went wrong... We\'ll get right on it'


def home(request):
    return render(request, 'home.html')


def user(request):
    lists = Songs_list.objects.filter(user=request.user, name='top 5').order_by('-id')[:5][::-1]

    list = []
    for e in lists:
        list.append(
            song_obj(Song.objects.filter(id=e.id).first().name, Song.objects.filter(id=e.id).first().artist.name))

    return render(request, 'usersongs.html', {'list': list})


def review(request):
    if request.method == 'POST':
        review_type = ReviewType(int(request.POST['type']))
        review_text = request.POST['reviewText']
        review_date = date.today()
        review_score = 1
        review_rating = float(request.POST['rating'])
        review_subj_auth = request.POST['by']
        review_subj = request.POST['subj']
        review_title = request.POST
        review_user = request.user

        review = Reviews.objects.create(
            name=review_title,
            text=review_text,
            date=review_date,
            rating=review_rating,
            score=review_score,
            user=request.user,
        )

        try:
            review.save()
        except Exception as ex:
            messages.info(request, ERROR_MESSAGE)
            handle_errors(ex)

        review_obj = object

        # TODO create review and save to db
        if review_type == ReviewType.ALBUM or review_type == ReviewType.ARTIST or review_type == ReviewType.SONG:
            artist = Artist.objects.filter(name=review_subj_auth).first()
            if review_type == ReviewType.ALBUM:
                album = Album.objects.filter(name=review_subj, artist=artist).first()
                review_obj = Album_Reviews.objects.create(
                    review=review,
                    album=album,
                )
            elif review_type == ReviewType.SONG:
                album = Album.objects.filter(name=review_subj, artist=artist).first()
                song = Song.object.create(
                    name=review_subj,
                    artist=artist,
                    album=album
                )
                review_obj = Song_Reviews.objects.create(
                    review=review,
                    song=song,
                )
            else:
                review_obj = Artist_Reviews.objects.create(
                    review=review,
                    artist=artist
                )
        else:
            # TODO implement playlist reviews
            pass

        try:
            review_obj.save()
        except Exception as ex:
            messages.info(request, ERROR_MESSAGE)
            handle_errors(ex)
        return redirect('review')

    else:
        return render(request,'createreview.html')


def user_reviews(request):
    return render(request,'userreviews.html',{'list':''})


def user_songs(request):
    return render(request,'usersongs.html',{'list':''})


def friends(request):
    return render(request,'userfriends.html',{'list':''})

def topsongs(request):
    # TODO This should be generalized for creating any type of list. We don't want duplicate songs in our db

    # This checks if request is POST if so gets data, if not redirects
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

        # TODO get this from spotify
        cur_alb = 'TBD'

        # TODO generalize this
        list = 'top 5'

        # adds each artist,song, etc. and checks for duplicates/handles erros
        for i in range(len(artists)):
            cur_art = artists[i]
            cur_song = songnames[i]
            artist = Artist.objects.create(name=cur_art)
            # add
            try:
                artist.save()
            except Exception as ex:
                if type(ex) == IntegrityError:
                    pass
                else:
                    messages.info(request, ERROR_MESSAGE)
                    handle_errors(ex)

            album = Album.objects.create(name=cur_alb, artist=artist)

            try:
                album.save()
            except Exception as ex:
                if type(ex) == IntegrityError:
                    pass
                else:
                    messages.info(request, ERROR_MESSAGE)
                    handle_errors(ex)

            song = Song.objects.create(name=cur_song, album=album, artist=artist)
            try:
                song.save()
            except Exception as ex:
                if type(ex) == IntegrityError:
                    pass
                else:
                    messages.info(request, ERROR_MESSAGE)
                    handle_errors(ex)

            songs = Songs_list.objects.create(user=request.user, name=list)
            songs.song.add(song)

            try:
                songs.save()
            except Exception as ex:
                if type(ex) == IntegrityError:
                    pass
                else:
                    messages.info(request, ERROR_MESSAGE)
                    handle_errors(ex)

        # TODO don't add duplicates, and replace if they are on the same list

        return redirect('user')

    else:
        return render(request, 'topsongs.html')


def trending(request):
    return render(request, 'trending.html')


def help(request):
    return render(request, 'help.html')


def handle_errors(ex):
    # TODO handle errors, possibly send an email to dev team
    pass


class ReviewType(Enum):
    ALBUM = 1
    SONG = 2
    PLAYLIST = 3
    ARTIST = 4


class song_obj:
    title = str
    artist = str

    def __init__(self, title, artist):
        self.title = title
        self.artist = artist
