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
        print(e.id)
        print(type(e))
        # print(getattr(e.song,'song_id'))
        list.append(
            SongObj(Song.objects.filter(id=e.id).first().get_name(), Song.objects.filter(id=e.id).first().get_artist().get_name()))

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
        review_title = request.POST['review-title']
        print(review_text)
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
            print(ex)
            handle_errors(ex)
        return redirect('reviews')

    else:
        return render(request, 'createreview.html')


def edit_review(request):
    return redirect('review')


def user_reviews(request):
    reviews = Reviews.objects.filter(user=request.user).order_by('date')[::-1]
    print(reviews)
    review_list = []
    for r in reviews:
        print(r.review_type)
        r_type = r.review_type
        if r_type == 'so':
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
                    username=request.user.username
                )
            )
        elif r_type == 'al':
            review_temp = Album_Reviews()
            review_temp = Album_Reviews.objects.filter(review=r).first()
            print('this works:', review_temp.get_album().get_name())
            album = review_temp.get_album().get_name()
            subj = '{0} by {1}'.format(
                album,
                review_temp.get_album().get_artist().get_name(),
            )
            review_list.append(
                PrintableReview(
                    subject=subj,
                    title=r.get_name(),
                    rating=r.get_rating(),
                    score=r.get_score(),
                    date=r.get_date(),
                    text=r.get_text(),
                    username=request.user.username
                )
            )
        elif r_type == 'ar':
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
                    username=request.user.username
                )
            )
        else:
            # review_list.append(
            #     Playlist_Reviews.objects.filter(review=r)
            # )
            pass
    print(len(reviews))
    return render(request, 'userreviews.html', {'list': review_list})


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
            if (artist[i] != '' and artist[i] != None) and (songnames[i] != '' and songnames[i] != None):
                cur_art = artists[i]
                cur_song = songnames[i]
                if Artist.objects.filter(name=cur_art).first() == None:
                    artist = Artist.objects.create(name=cur_art)
                    # add
                    Album.objects.create(name=cur_alb, artist=artist)
                    if Album.objects.filter(name=cur_alb).count() == 0:
                        Album.objects.create(name=cur_alb, artist=artist)
                else:
                    artist = Artist.objects.filter(name=cur_art).first()
                    if Album.objects.filter(name=cur_alb, artist=artist).first() == None:
                        Album.objects.create(name=cur_alb, artist=artist)

                artist = Artist.objects.filter(name=cur_art).first()
                album = Album.objects.filter(name=cur_alb, artist=artist).first()
                if Song.objects.filter(name=cur_song, album=album, artist=artist).first() == None:
                    song = Song.objects.create(name=cur_song, album=album, artist=artist)
                    songs = Songs_list.objects.create(user=request.user, name=list)
                    songs.song.add(song)
                else:
                    song = Song.objects.filter(name=cur_song, artist=artist, album=album).first()
                    print(song)
                    songs = Songs_list.objects.create(user=request.user, name=list)
                    songs.song.add(song)
            # TODO don't add duplicates, and replace if they are on the same list
            else:
                messages.info(request, ERROR_MESSAGE)
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
    username = str

    def __init__(self, subject, title, rating, score, date, text, username):
        self.subject = subject
        self.title = title
        self.rating = rating
        self.score = score
        self.date = date
        self.text = text
        self.username = username
