# Generated by Django 3.1.5 on 2021-02-01 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sandwich',
            name='ingredients',
            field=models.ManyToManyField(blank=True, to='client.Ingredients'),
        ),
    ]
