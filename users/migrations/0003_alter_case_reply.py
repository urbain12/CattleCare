# Generated by Django 3.2.10 on 2023-01-13 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_case_sector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='reply',
            field=models.TextField(blank=True, default='None', null=True),
        ),
    ]
