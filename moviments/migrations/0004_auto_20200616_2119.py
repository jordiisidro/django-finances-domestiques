# Generated by Django 3.0.5 on 2020-06-16 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moviments', '0003_auto_20200531_1235'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='moviment',
            options={'ordering': ['-dataMoviment', 'caixa'], 'verbose_name_plural': 'Moviments'},
        ),
    ]
