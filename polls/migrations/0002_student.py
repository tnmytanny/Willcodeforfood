# Generated by Django 2.1.2 on 2018-10-23 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StudentID', models.CharField(max_length=20)),
                ('Name', models.CharField(max_length=30)),
                ('Password', models.CharField(max_length=20)),
            ],
        ),
    ]