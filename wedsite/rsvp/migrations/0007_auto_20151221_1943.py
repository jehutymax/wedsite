# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0006_auto_20151221_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='address1',
            field=models.CharField(null=True, max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='address2',
            field=models.CharField(null=True, max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='city',
            field=models.CharField(null=True, max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='country',
            field=models.CharField(null=True, max_length=12, blank=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='email',
            field=models.CharField(null=True, max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='name',
            field=models.CharField(null=True, max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='state',
            field=models.CharField(null=True, max_length=2, blank=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='zipcode',
            field=models.CharField(null=True, max_length=12, blank=True),
        ),
        migrations.AlterField(
            model_name='rsvp',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 22, 0, 43, 1, 859712, tzinfo=utc)),
        ),
    ]
