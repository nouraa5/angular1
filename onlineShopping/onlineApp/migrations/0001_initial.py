# Generated by Django 5.0.3 on 2024-04-04 11:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('brand_type', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('brand_title', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=150)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('product_desc', models.CharField(max_length=150)),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('product_keywords', models.TextField(blank=True, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='onlineApp.brands')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]