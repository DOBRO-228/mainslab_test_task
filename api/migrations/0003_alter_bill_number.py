# Generated by Django 4.0.4 on 2022-05-07 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_bill_sum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='number',
            field=models.IntegerField(),
        ),
    ]
