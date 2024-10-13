# Generated by Django 5.1.2 on 2024-10-13 05:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eco_webapp', '0002_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField()),
                ('buyer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_buyer', to='Eco_webapp.userdetails')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_products', to='Eco_webapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='Eco_certifications',
            fields=[
                ('certification_id', models.AutoField(primary_key=True, serialize=False)),
                ('certification_name', models.CharField(max_length=255)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certifications', to='Eco_webapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('buyer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_buyer', to='Eco_webapp.userdetails')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='Eco_webapp.product')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('wishlist_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlist_products', to='Eco_webapp.product')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wishlists', to='Eco_webapp.userdetails')),
            ],
        ),
    ]
