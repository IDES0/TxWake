# Generated by Django 4.2.15 on 2024-09-17 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('txwake', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('subscribed_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
