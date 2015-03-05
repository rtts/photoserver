# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import photoserver.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('game_name', models.CharField(max_length=255)),
                ('partner_name', models.SlugField()),
                ('game_id', models.IntegerField()),
                ('album_id', models.CharField(blank=True, max_length=255)),
                ('album_url', models.CharField(max_length=255, default='5gsl0SkMTiW72IRrSjLD5xrjig2j9o4w')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('source', models.ImageField(upload_to=photoserver.models.photo_location)),
                ('comment', models.CharField(blank=True, max_length=255)),
                ('album', models.ForeignKey(to='photoserver.Album', related_name='photos')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='album',
            unique_together=set([('partner_name', 'game_id')]),
        ),
    ]
