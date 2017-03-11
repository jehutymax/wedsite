# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0004_auto_20151127_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='caption',
            field=models.CharField(max_length=80, null=True),
        ),
    ]
