# Generated by Django 5.1.3 on 2025-03-04 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('enrollment', '0001_initial'),
        ('users', '0002_student_level'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together={('student', 'course')},
        ),
    ]
