# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import photoserver.models


class Migration(migrations.Migration):

    dependencies = [
        ('photoserver', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_url',
            field=models.CharField(default=photoserver.models.generate_album_url, max_length=255),
            preserve_default=True,
        ),
    ]
