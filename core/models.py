from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=2, default='N/A')
    is_active = models.BooleanField(default=True)
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='students',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} — {self.name}"
    
