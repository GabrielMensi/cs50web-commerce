# Generated by Django 5.0.4 on 2024-05-03 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]