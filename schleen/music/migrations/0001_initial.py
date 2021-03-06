# Generated by Django 3.0.3 on 2020-03-18 02:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_type', models.CharField(choices=[('al', 'AL'), ('ar', 'AR'), ('so', 'SO'), ('pl', 'PL')], default='al', max_length=2)),
                ('name', models.CharField(max_length=80)),
                ('text', models.TextField()),
                ('date', models.DateField()),
                ('date_modified', models.DateField()),
                ('rating', models.FloatField()),
                ('score', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='written_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Songs_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('album', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='album', to='music.Album')),
                ('artist', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='artist', to='music.Artist')),
                ('songs', models.ManyToManyField(related_name='song', to='music.Songs_list')),
            ],
            options={
                'unique_together': {('artist', 'name', 'album')},
            },
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='music.Artist'),
        ),
        migrations.CreateModel(
            name='Song_Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Reviews')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Song')),
            ],
            options={
                'unique_together': {('song', 'review')},
            },
        ),
        migrations.CreateModel(
            name='Artist_Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Artist')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Reviews')),
            ],
            options={
                'unique_together': {('artist', 'review')},
            },
        ),
        migrations.CreateModel(
            name='Album_Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Album')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Reviews')),
            ],
            options={
                'unique_together': {('album', 'review')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='album',
            unique_together={('artist', 'name')},
        ),
    ]
