# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import photoserver.models


class Migration(migrations.Migration):

    dependencies = [
        ('photoserver', '0002_auto_20160107_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('source', models.FileField(upload_to=photoserver.models.video_location)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('comment', models.CharField(blank=True, max_length=255)),
                ('album', models.ForeignKey(to='photoserver.Album', related_name='videos')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
