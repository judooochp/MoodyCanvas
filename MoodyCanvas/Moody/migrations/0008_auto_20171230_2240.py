# Generated by Django 2.0 on 2017-12-31 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Moody', '0007_auto_20171230_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='verif',
            name='verif_max',
            field=models.IntegerField(default=-84),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='verif',
            name='verif_min',
            field=models.IntegerField(default=-84),
            preserve_default=False,
        ),
    ]