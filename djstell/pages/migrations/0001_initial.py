# Generated by Django 2.1.4 on 2019-01-01 17:40

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import djstell.pages.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(db_index=True, max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('comments', models.BooleanField(default=False)),
                ('sort', models.IntegerField(default=500)),
                ('sitemap', models.BooleanField(default=True)),
                ('lang', models.CharField(max_length=5)),
                ('copyright', models.TextField()),
                ('meta', models.TextField()),
                ('scripts', models.TextField()),
                ('style', models.TextField()),
                ('features', models.TextField()),
            ],
            bases=(models.Model, djstell.pages.models.ModelMixin),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(db_index=True, max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('when', models.DateTimeField(db_index=True)),
                ('draft', models.BooleanField()),
                ('text', models.TextField()),
                ('slug', models.CharField(db_index=True, max_length=200)),
                ('comments_closed', models.BooleanField()),
                ('features', models.TextField()),
            ],
            bases=(models.Model, djstell.pages.models.ModelMixin),
            managers=[
                ('all_entries', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('href', models.CharField(max_length=1000)),
                ('slug', models.CharField(max_length=30)),
                ('text', models.CharField(max_length=200)),
                ('sidebar', models.BooleanField(default=False)),
            ],
            bases=(models.Model, djstell.pages.models.ModelMixin),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('sort', models.IntegerField(default=500)),
                ('sitemap', models.BooleanField(default=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.Article')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50, null=True)),
                ('about', models.TextField(null=True)),
                ('sidebar', models.BooleanField()),
            ],
            bases=(models.Model, djstell.pages.models.ModelMixin),
        ),
        migrations.CreateModel(
            name='Via',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('href', models.CharField(max_length=1000, null=True)),
                ('text', models.CharField(max_length=200, null=True)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.Entry')),
                ('link', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pages.Link')),
            ],
        ),
        migrations.CreateModel(
            name='WhatWhen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField()),
                ('what', models.CharField(max_length=200)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.Article')),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(to='pages.Tag'),
        ),
    ]
