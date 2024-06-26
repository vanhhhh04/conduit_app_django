# Generated by Django 5.0.4 on 2024-04-16 03:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('body', models.TextField()),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
                ('author', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdAt', models.DateTimeField()),
                ('updatedAt', models.DateTimeField()),
                ('body', models.TextField()),
                ('author', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='articles.article')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=100)),
                ('article', models.ManyToManyField(to='articles.article')),
            ],
        ),
    ]
