from django.db import models
from  users.models import Tutor
from django.apps import apps

# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    level = models.CharField(max_length=200,  choices=[('100', '100'), ('200', '200'), ('300', '300')])
    department = models.CharField(max_length=200 , default='Computer Science')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='courses') 

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the course first

        # Auto-enroll all matching students after saving the course
        self.auto_enroll_students()

    def auto_enroll_students(self):
        """Automatically enroll all students who match the course criteria."""
        Student = apps.get_model('users', 'Student')
        Enrollment = apps.get_model('enrollment', 'Enrollment')

        matching_students = Student.objects.filter(level=self.level, department=self.department)
        for student in matching_students:
            Enrollment.objects.get_or_create(student=student, course=self)

    def __str__(self):
        return self.code
