# Generated by Django 4.1.7 on 2023-03-22 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_products_stock_delete_productsstorage'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='sell_price',
            field=models.FloatField(default=0),
        ),
    ]
