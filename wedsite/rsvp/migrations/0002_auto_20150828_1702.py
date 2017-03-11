# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rsvp',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 28, 21, 1, 43, 7221, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rsvp',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 28, 21, 2, 1, 758276, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
