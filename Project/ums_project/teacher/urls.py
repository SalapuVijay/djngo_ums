from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('upload-cgpa/', views.upload_cgpa, name='upload_cgpa'),
    path('send-message/', views.send_message, name='send_message'),
    path('add-timetable/', views.add_timetable, name='add_timetable'),
    path('courses/', views.manage_courses, name='manage_courses'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
]