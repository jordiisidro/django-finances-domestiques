# Generated by Django 3.0.5 on 2020-06-01 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mov', '0007_caixa_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='caixa',
            name='banc',
            field=models.BooleanField(default=True),
        ),
    ]
