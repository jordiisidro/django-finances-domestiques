# Generated by Django 3.0.5 on 2020-06-09 13:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mov', '0008_caixa_banc'),
    ]

    operations = [
        migrations.AddField(
            model_name='caixa',
            name='usuaris',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
