# Generated by Django 3.2.4 on 2021-06-14 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('categoryfather', models.IntegerField(blank=True, db_column='CategoryFather', null=True)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('phone', models.CharField(blank=True, db_column='Phone', max_length=255, null=True)),
                ('email', models.CharField(blank=True, db_column='Email', max_length=255, null=True)),
            ],
            options={
                'db_table': 'supplier',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('price', models.FloatField(blank=True, db_column='Price', null=True)),
                ('name', models.CharField(blank=True, db_column='Name', max_length=255, null=True)),
                ('quantity', models.IntegerField(blank=True, db_column='Quantity', null=True)),
                ('img', models.CharField(blank=True, db_column='Img', max_length=255, null=True)),
                ('desc', models.CharField(blank=True, db_column='Desc', max_length=255, null=True)),
                ('categoryid', models.ForeignKey(db_column='CategoryID', on_delete=django.db.models.deletion.DO_NOTHING, to='product.category')),
                ('supplierid', models.ForeignKey(db_column='SupplierID', on_delete=django.db.models.deletion.DO_NOTHING, to='product.supplier')),
            ],
            options={
                'db_table': 'product',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('outprice', models.FloatField(blank=True, db_column='Outprice', null=True)),
                ('productid', models.ForeignKey(db_column='ProductID', on_delete=django.db.models.deletion.DO_NOTHING, to='product.product')),
            ],
            options={
                'db_table': 'item',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('content', models.CharField(blank=True, db_column='Content', max_length=255, null=True)),
                ('time', models.DateField(blank=True, db_column='Time', null=True)),
                ('state', models.CharField(blank=True, db_column='State', max_length=255, null=True)),
                ('itemid', models.ForeignKey(db_column='ItemID', on_delete=django.db.models.deletion.DO_NOTHING, to='product.item')),
                ('userid', models.ForeignKey(blank=True, db_column='UserID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user.user')),
            ],
            options={
                'db_table': 'comment',
            },
        ),
    ]
