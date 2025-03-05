from django.db import models
import random
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.apps import apps

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_name = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=200, choices=[('100', '100'), ('200', '200'), ('300', '300')], blank=False)
    gender = models.CharField(max_length=200, choices=[('Male', 'Male'), ('Female', 'Female'), ('Rather not say', 'Rather not say')], blank=False)
    department = models.CharField(max_length=200 , default='Computer Science')
    registration_number = models.CharField(max_length=200)
    username = models.CharField(max_length=100, unique=True, blank=True)
    profile_pic = models.ImageField(blank=True)

    def save(self, *args, **kwargs):
        if not self.profile_pic:
            self.profile_pic = 'default.jpg' if self.gender == 'Male' else 'default_f.jpg'
        
        if Tutor.objects.filter(user=self.user).exists():
            raise ValidationError("This user is already assigned as a Tutor and cannot be a Student.")

        self.username = self.generate_username()
        
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.username = self.username

        self.user.save()
 
        super().save(*args, **kwargs)
        self.auto_enroll()

    def generate_username(self):
        return f"{self.first_name.upper()[:2]}{random.randint(111,999)}{self.last_name.upper()[:2]}{random.randint(11,99)}"
   
            
    def auto_enroll(self):
        Course = apps.get_model('courses', 'Course') 
        Enrollment = apps.get_model('enrollment', 'Enrollment')

        matching_courses = Course.objects.filter(level=self.level, department=self.department)
        for course in matching_courses:
            Enrollment.objects.get_or_create(student=self, course=course)
            
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True, blank=True)
    other_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=200, choices=[('Male', 'Male'), ('Female', 'Female'), ('Rather not say', 'Rather not say')], blank=True)
    profile_pic = models.ImageField(blank=True,null=True)
    
    
    def save(self, *args, **kwargs):
        if not self.profile_pic:
            self.profile_pic = 'default.jpg' if self.gender == 'Male' else 'default_f.jpg'
        
        if Student.objects.filter(user=self.user).exists():
            raise ValidationError("This user is already assigned as a Student and cannot be a Tutor.")

        if not self.username:
            self.username = self.generate_username()
        
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.username = self.username
        self.user.is_staff = True
        self.user.save()

        super().save(*args, **kwargs)

    def generate_username(self):
        return f"{self.first_name.upper()[:2]}{random.randint(111,999)}{self.last_name.upper()[:2]}{random.randint(11,99)}"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
