# Generated by Django 5.0.2 on 2024-02-22 06:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('seller', '0004_alter_products_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.FloatField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.products')),
            ],
            options={
                'db_table': 'cart_tb',
            },
        ),
    ]
