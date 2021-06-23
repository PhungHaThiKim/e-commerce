# Generated by Django 3.2.4 on 2021-06-14 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('user', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('state', models.IntegerField(blank=True, db_column='State', null=True)),
                ('userid', models.ForeignKey(blank=True, db_column='UserID', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='user.user')),
            ],
            options={
                'db_table': 'cart',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(blank=True, db_column='Quantity', null=True)),
                ('cost', models.FloatField(blank=True, db_column='Cost', null=True)),
                ('cartid', models.ForeignKey(db_column='CartID', on_delete=django.db.models.deletion.DO_NOTHING, to='cart.cart')),
                ('itemid', models.ForeignKey(db_column='ItemID', on_delete=django.db.models.deletion.DO_NOTHING, to='product.item')),
            ],
            options={
                'db_table': 'cart_item',
            },
        ),
    ]