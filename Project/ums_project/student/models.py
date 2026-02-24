from django.db import models
from django.conf import settings

class Course(models.Model):
    name = models.CharField(max_length=100)
    semester = models.IntegerField()

    def __str__(self):
        return self.name


class Attendance(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_classes = models.IntegerField(default=0)
    attended_classes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.username} - {self.course.name}"

    @property
    def attendance_percentage(self):
        if self.total_classes == 0:
            return 0
        return round((self.attended_classes / self.total_classes) * 100, 2)

    class Meta:
        unique_together = ('student', 'course')
        verbose_name_plural = 'Attendances'


class Result(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cgpa = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.student.username} - {self.cgpa}"


class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.course.name} - {self.day}"

    class Meta:
        verbose_name_plural = 'Timetables'
        ordering = ['day', 'start_time']


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"

    class Meta:
        ordering = ['-timestamp']