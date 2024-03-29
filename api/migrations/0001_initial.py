# Generated by Django 2.2.2 on 2019-06-09 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('calorie', models.IntegerField()),
                ('unitName', models.CharField(choices=[('KJ', 'KJ')], max_length=50)),
                ('quantity', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('breakfast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='breakfast', to='api.Food')),
                ('dinner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dinner', to='api.Food')),
                ('lunch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lunch', to='api.Food')),
                ('snacks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='snacks', to='api.Food')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User')),
            ],
            options={
                'unique_together': {('username', 'date')},
            },
        ),
    ]
