# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReceiveResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fee_percent', models.IntegerField()),
                ('destination_address', models.CharField(max_length=35)),
                ('input_address', models.CharField(max_length=35)),
                ('callback_url', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
