# Generated by Django 4.1.1 on 2022-11-26 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_rename_tsop_list_product_stop_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]