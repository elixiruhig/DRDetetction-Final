# Generated by Django 2.2.1 on 2020-04-05 07:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DiabeticRetinopathy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 5, 7, 28, 13, 79092)),
        ),
    ]
