# Generated by Django 2.1.2 on 2018-11-24 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_auto_20181124_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='allprojects',
            name='tag',
            field=models.CharField(default='', max_length=50),
        ),
    ]
