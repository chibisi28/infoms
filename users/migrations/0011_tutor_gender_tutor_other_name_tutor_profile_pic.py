# Generated by Django 5.1.3 on 2025-03-04 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_student_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Rather not say', 'Rather not say')], max_length=200),
        ),
        migrations.AddField(
            model_name='tutor',
            name='other_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='tutor',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=''),
        ),
    ]
