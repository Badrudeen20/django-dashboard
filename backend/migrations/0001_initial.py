# Generated by Django 5.1.1 on 2024-09-25 03:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(max_length=255)),
                ('moduleType', models.CharField(default=1, max_length=255)),
                ('url', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(default=1, max_length=255)),
                ('pid', models.CharField(blank=True, max_length=255)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='GroupPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mpid', models.CharField(blank=True, max_length=255)),
                ('permission', models.CharField(max_length=255)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('rid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='auth.group')),
                ('mid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='backend.module')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
