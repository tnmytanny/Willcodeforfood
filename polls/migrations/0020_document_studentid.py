# Generated by Django 2.1.2 on 2018-11-25 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0019_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='StudentID',
            field=models.CharField(default='', max_length=10),
        ),
    ]