# Generated by Django 2.2.2 on 2019-07-07 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notecheck',
            old_name='audioFile',
            new_name='audio_file',
        ),
        migrations.RemoveField(
            model_name='notecheck',
            name='notesDisplay',
        ),
        migrations.RemoveField(
            model_name='notecheck',
            name='pageTitle',
        ),
    ]
