# Generated by Django 3.0.5 on 2020-05-31 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mov', '0002_auto_20200531_1235'),
        ('moviments', '0002_auto_20200519_2234'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='moviment',
            unique_together={('dataMoviment', 'detallMoviment', 'formaPagament', 'caixa')},
        ),
    ]
