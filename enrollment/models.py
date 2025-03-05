from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import Student
from courses.models import Course

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    test = models.FloatField(default=0, validators=[MaxValueValidator(30), MinValueValidator(0)])
    exam = models.FloatField(default=0, validators=[MaxValueValidator(70), MinValueValidator(0)])

    class Meta:
        unique_together = ('student', 'course')

    def clean(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        """Ensure that only courses of the same level as the student are allowed."""
        if self.student.level != self.course.level:
            raise ValidationError(f"{self.course} is not available for {self.student}'s level.")
        if user:
            # Restrict edits of test and exam scores
            if user != self.course.tutor:
                if user.is_superuser:
                    raise ValidationError("Even the admin cannot edit this student's scores.")
                raise ValidationError("Only the assigned tutor can edit this student's scores.")

    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        if user:
            # Restrict edits of test and exam scores
            if user != self.course.tutor:
                if user.is_superuser:
                    raise ValidationError("Even the admin cannot edit this student's scores.")
                raise ValidationError("Only the assigned tutor can edit this student's scores.")
        # Proceed with saving
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.student} enrolled in {self.course}"
