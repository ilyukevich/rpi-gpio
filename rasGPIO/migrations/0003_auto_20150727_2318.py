# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rasGPIO', '0002_auto_20150727_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='controlluser',
            name='privig',
            field=models.IntegerField(default=4),
        ),
    ]
