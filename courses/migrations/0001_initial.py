# Generated by Django 5.1.3 on 2025-03-04 12:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=200)),
                ('level', models.CharField(choices=[('100', '100'), ('200', '200'), ('300', '300')], max_length=200)),
                ('department', models.CharField(default='Computer Science', max_length=200)),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='users.tutor')),
            ],
        ),
    ]
