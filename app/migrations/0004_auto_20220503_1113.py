# Generated by Django 3.2.12 on 2022-05-03 05:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_record'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='record',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='record',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
