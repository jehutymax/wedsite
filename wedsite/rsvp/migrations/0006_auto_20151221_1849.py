# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0005_event_caption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='attending',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='rsvp',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 21, 23, 49, 24, 977114, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rsvp',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
