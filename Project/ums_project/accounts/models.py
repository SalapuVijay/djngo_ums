from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    SEMESTER_CHOICES = (
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
        (7, 'Semester 7'),
        (8, 'Semester 8'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE)
    reg_no = models.CharField(max_length=7, unique=True)
    semester = models.IntegerField(choices=SEMESTER_CHOICES, default=1, help_text="Select your current semester")

    def __str__(self):
        return self.username