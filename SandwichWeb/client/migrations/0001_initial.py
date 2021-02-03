# Generated by Django 3.1.5 on 2021-02-03 03:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id_ingredients', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id_order', models.AutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('client_name', models.CharField(max_length=100)),
                ('total', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id_size', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Sandwich',
            fields=[
                ('id_sandwich', models.AutoField(primary_key=True, serialize=False)),
                ('total', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ingredients', models.ManyToManyField(blank=True, to='client.Ingredients')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.order')),
                ('size', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='client.size')),
            ],
        ),
    ]
