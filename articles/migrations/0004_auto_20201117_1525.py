# Generated by Django 2.2 on 2020-11-17 20:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20201117_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_uploaded',
            field=models.DateField(default=datetime.datetime(2020, 11, 17, 20, 25, 9, 807299, tzinfo=utc)),
        ),
    ]
