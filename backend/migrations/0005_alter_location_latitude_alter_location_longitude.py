# Generated by Django 4.1.1 on 2022-11-25 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_user_phone_alter_cartobject_confirm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='latitude',
            field=models.CharField(max_length=400, null=True, verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='location',
            name='longitude',
            field=models.CharField(max_length=400, null=True, verbose_name='Longitude'),
        ),
    ]
