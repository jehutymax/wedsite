# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rsvp', '0002_auto_20150828_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rsvp',
            name='guest',
        ),
        migrations.AddField(
            model_name='guest',
            name='first_visit',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='guest',
            name='user',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rsvp',
            name='going',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='rsvp',
            name='person',
            field=models.ForeignKey(default=0, to='rsvp.Person'),
            preserve_default=False,
        ),
    ]
