# Generated by Django 2.2 on 2020-11-17 18:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_uploaded',
            field=models.DateField(default=datetime.datetime(2020, 11, 17, 18, 21, 24, 430805, tzinfo=utc)),
        ),
    ]