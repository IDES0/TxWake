# Generated by Django 4.2.15 on 2024-09-17 23:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('txwake', '0003_rename_subscribed_on_emailsubscription_date_subscribed_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Signup',
            new_name='BoatPullSignup',
        ),
    ]
