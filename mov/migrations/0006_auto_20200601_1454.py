# Generated by Django 3.0.5 on 2020-06-01 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mov', '0005_auto_20200601_1451'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='detallmoviment',
            unique_together={('subgrupMoviment', 'descripcio')},
        ),
    ]