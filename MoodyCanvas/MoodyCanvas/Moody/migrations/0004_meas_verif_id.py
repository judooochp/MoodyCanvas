# Generated by Django 2.0 on 2017-12-29 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Moody', '0003_auto_20171227_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='meas',
            name='verif_id',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to='Moody.Verif'),
            preserve_default=False,
        ),
    ]
