# Generated by Django 4.2.3 on 2023-10-03 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appweb', '0002_alter_client_genre'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prospection',
            name='date',
        ),
        migrations.RemoveField(
            model_name='prospection',
            name='user',
        ),
    ]
