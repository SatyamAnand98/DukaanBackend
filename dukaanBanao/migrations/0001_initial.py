# Generated by Django 4.0.1 on 2022-01-24 10:07

from django.db import migrations, models
import django.db.models.deletion
import dukaanBanao.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('phNumber', models.BigIntegerField(unique=True)),
                ('otp', models.IntegerField()),
                ('token', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, upload_to=dukaanBanao.models.upload_path)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=50)),
                ('MRP', models.DecimalField(decimal_places=4, max_digits=8)),
                ('SP', models.DecimalField(decimal_places=4, max_digits=8)),
                ('cat', models.CharField(max_length=20)),
                ('image', models.ManyToManyField(to='dukaanBanao.image')),
            ],
        ),
        migrations.CreateModel(
            name='store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storeName', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=50)),
                ('storeURL', models.URLField(max_length=50, unique=True)),
                ('account_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dukaanBanao.account')),
                ('product_ID', models.ManyToManyField(to='dukaanBanao.product')),
            ],
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryName', models.CharField(max_length=20)),
                ('product_id', models.ManyToManyField(to='dukaanBanao.product')),
            ],
        ),
    ]
