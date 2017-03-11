# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0003_auto_20151127_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='address1',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='address2',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='city',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='country',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='email',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='state',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='guest',
            name='zipcode',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
