from django.contrib import admin
from .models import Course, Attendance, Result, Timetable, Message


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'semester']
    list_filter = ['semester']
    search_fields = ['name']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'attended_classes', 'total_classes', 'attendance_percentage']
    list_filter = ['course', 'student']
    search_fields = ['student__username', 'course__name']
    readonly_fields = ['attendance_percentage']


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'cgpa']
    list_filter = ['cgpa']
    search_fields = ['student__username']


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['course', 'day', 'start_time', 'end_time', 'room']
    list_filter = ['day', 'course']
    search_fields = ['course__name', 'room']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'timestamp', 'is_read']
    list_filter = ['is_read', 'timestamp', 'sender']
    search_fields = ['sender__username', 'receiver__username', 'content']
    readonly_fields = ['timestamp']
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, "Selected messages marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"
