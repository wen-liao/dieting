# Generated by Django 2.1.8 on 2019-06-11 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20190611_0329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodrecord',
            name='unitName',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='sportsrecord',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='sportsrecord',
            name='unitName',
            field=models.CharField(max_length=50),
        ),
    ]
