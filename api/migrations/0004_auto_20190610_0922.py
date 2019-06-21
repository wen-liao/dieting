# Generated by Django 2.1.8 on 2019-06-10 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190610_0640'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('caloriePerGram', models.IntegerField()),
                ('food_type', models.CharField(choices=[('dinner', 'dinner'), ('snacks', 'snacks')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unitName', models.CharField(max_length=50)),
                ('gramPerUnit', models.IntegerField()),
                ('upperLimit', models.IntegerField()),
                ('step', models.IntegerField()),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Food')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='daily',
            unique_together={('username', 'date')},
        ),
        migrations.AlterUniqueTogether(
            name='unit',
            unique_together={('name', 'unitName')},
        ),
    ]
