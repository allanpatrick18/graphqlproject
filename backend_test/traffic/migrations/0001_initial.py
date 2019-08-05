# Generated by Django 2.2.3 on 2019-08-01 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender_enum', models.CharField(choices=[('MALE', 0), ('FEMALE', 1), ('UNIDENTIFIED', 2)], default=2, max_length=255)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100)),
                ('topic', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.User')),
                ('website', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='traffic.Website')),
            ],
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('users_count', models.IntegerField()),
                ('websites_count', models.IntegerField()),
                ('visits_count', models.IntegerField()),
                ('users', models.ManyToManyField(to='traffic.User')),
                ('visits', models.ManyToManyField(to='traffic.Visit')),
                ('websites', models.ManyToManyField(to='traffic.Website')),
            ],
        ),
    ]
