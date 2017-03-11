# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0007_auto_20151221_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('event', models.ForeignKey(to='rsvp.Event')),
                ('guest', models.ForeignKey(to='rsvp.Guest')),
            ],
        ),
        migrations.AlterField(
            model_name='rsvp',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 6, 1, 18, 22, 52, 262763, tzinfo=utc)),
        ),
    ]
