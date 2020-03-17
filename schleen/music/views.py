from django.shortcuts import render, redirect
from .models import Song, Songs_list, Artist, Album, Reviews, Album_Reviews, Artist_Reviews, Song_Reviews
from django.db import IntegrityError
from django.contrib import messages
from enum import Enum
from datetime import date

# TODO disalow empty fields and duplicate songs

ERROR_MESSAGE = 'Uh oh, something went wrong... We\'ll get right on it'
REVIEW_TYPE = {'s': 'Song', 'ar': 'Artist', 'al': 'Album', 'p': 'Playlist'}


def home(request):
    return render(request, 'home.html')


def user(request):
    lists = Songs_list.objects.filter(user=request.user, name='top 5').order_by('-id')[:5][::-1]

    list = []
    for e in lists:
        list.append(
            SongObj(Song.objects.filter(id=e.id).first().name, Song.objects.filter(id=e.id).first().artist.name))

    return render(request, 'usersongs.html', {'list': list})


def review(request):
    if request.method == 'POST':
        # review_type: artist, album, song, or playlist
        review_type = request.POST['review-type']
        review_text = request.POST['review-text']
        review_date = date.today()
        # review_score: points added or subtracted to review by community
        review_score = 1
        # review_rating: reviewer's rating of subject out of 10
        review_rating = float(request.POST['rating'])
        # review_subj_auth: artist for artist, album, song reviews; user for playlist reviewa
        review_subj_auth = request.POST['subj-auth']
        # review_subj_container: album (only for song reviews)
        review_subj_container = None
        if review_type == REVIEW_TYPE['s']:
            review_subj_container = request.POST['subj-container']
        # review_subj: song or album or playlist (N/A for artist reviews)
        review_subj = request.POST['subj']
        review_title = request.POST
        review_user = request.user

        review_base = Reviews.objects.create(
            name=review_title,
            text=review_text,
            date=review_date,
            rating=review_rating,
            score=review_score,
            user=review_user,
        )

        try:
            review_base.save()
        except Exception as ex:
            messages.info(request, ERROR_MESSAGE)
            handle_errors(ex)

        review_obj = None

        if review_type != REVIEW_TYPE['p']:
            # check if artist already exists in db
            if Artist.objects.filter(name=review_subj_auth).count() > 0:
                artist = Artist.objects.filter(name=review_subj_auth).first()
            # if not, add it
            else:
                artist = Artist.objects.create(
                    name=review_subj_auth
                )
            if review_type == REVIEW_TYPE['al']:
                # check if album already exists in db
                if Album.objects.filter(name=review_subj, artist=artist).count() > 0:
                    album = Album.objects.filter(name=review_subj, artist=artist).first()
                # if not, add it
                else:
                    album = Album.objects.create(
                        name=review_subj,
                        artist=artist
                    )
                review_obj = Album_Reviews.objects.create(
                    review=review_base,
                    album=album,
                )
            elif review_type == REVIEW_TYPE['s']:
                # check if album already exists in db
                if Album.objects.filter(name=review_subj_container, artist=artist).count() > 0:
                    album = Album.objects.filter(name=review_subj_container, artist=artist).first()
                # if not, add it
                else:
                    album = Album.objects.create(
                        name=review_subj_container,
                        artist=artist
                    )
                # check if song already exists in db
                if Song.objects.filter(name=review_subj, album=album, artist=artist).count() > 0:
                    song = Song.objects.filter(name=review_subj, album=album, artist=artist).first()
                # if not, add it
                else:
                    song = Song.objects.create(
                        name=review_subj,
                        artist=artist,
                        album=album
                    )
                review_obj = Song_Reviews.objects.create(
                    review=review_base,
                    song=song,
                )
            else:
                review_obj = Artist_Reviews.objects.create(
                    review=review_base,
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
        return render(request, 'createreview.html')


def user_reviews(request):
    reviews = Reviews.objects.filter(user=request.user).order_by('date')[::-1]

    review_list = []
    for r in reviews:
        r_type = r.review_type
        if r_type == 'SO':
            review_temp = Song_Reviews.objects.filter(review=r).first()
            song = Song.objects.filter(id=review_temp.song_id).first()
            subj = '{0} by {1} from the album {2}'.format(
                song.name,
                Artist.objects.filter(id=song.artist_id).name,
                Album.objects.filter(id=song.album_id).name,
            )

            review_list.append(
                PrintableReview(
                    subject=subj,
                    title=r.name,
                    rating=r.rating,
                    score=r.score,
                    date=r.date,
                    text=r.text,
                )
            )
        elif r_type == 'AL':
            review_temp = Album_Reviews.objects.filter(review=r).first()
            album = Album.objects.filter(id=review_temp.album_id).first()
            subj = '{0} by {1}'.format(
                album.name,
                Artist.objects.filter(id=album.artist_id).name,
            )
            review_list.append(
                PrintableReview(
                    subject=subj,
                    title=r.name,
                    rating=r.rating,
                    score=r.score,
                    date=r.date,
                    text=r.text,
                )
            )
        elif r_type == 'AR':
            review_temp = Artist_Reviews.objects.filter(review=r).first()
            artist = Artist.objects.filter(id=review_temp.artist_id).first()
            subj = artist.name
            review_list.append(
                PrintableReview(
                    subject=subj,
                    title=r.name,
                    rating=r.rating,
                    score=r.score,
                    date=r.date,
                    text=r.text,
                )
            )
        else:
            # review_list.append(
            #     Playlist_Reviews.objects.filter(review=r)
            # )
            pass

    return render(request, 'userreviews.html', {'list': ''})


def user_songs(request):
    return render(request, 'usersongs.html', {'list': ''})


def friends(request):
    return render(request, 'userfriends.html', {'list': ''})


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

        # adds each artist,song, etc. and checks for duplicates/handles errors
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


class SongObj:
    title = str
    artist = str

    def __init__(self, title, artist):
        self.title = title
        self.artist = artist


class PrintableReview:
    subject = str
    title = str
    rating = float
    score = int
    date = str
    text = str

    def __init__(self, subject, title, rating, score, date, text):
        self.subject = subject
        self.title = title
        self.rating = rating
        self.score = score
        self.date = date
        self.text = text
