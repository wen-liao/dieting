# Generated by Django 2.1.8 on 2019-06-11 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20190611_0221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='id',
        ),
        migrations.AlterField(
            model_name='food',
            name='name',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
