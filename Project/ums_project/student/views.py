from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from student.models import Attendance, Course, Result, Message, Timetable


@login_required
def student_dashboard(request):
    try:
        attendance = Attendance.objects.filter(student=request.user)
        result = Result.objects.filter(student=request.user).first()
        user_messages = Message.objects.filter(receiver=request.user).order_by('-timestamp')
        timetable = Timetable.objects.all().order_by('day', 'start_time')
        
        
        student_semester = request.user.semester
        courses = Course.objects.filter(semester=student_semester).order_by('name')

   
        unread_messages = user_messages.filter(is_read=False)
        unread_messages.update(is_read=True)

        return render(request, 'student/dashboard.html', {
            'attendance': attendance,
            'result': result,
            'messages': user_messages,
            'timetable': timetable,
            'courses': courses,
            'student_semester': student_semester,
            'unread_count': unread_messages.count()
        })
    except Exception as e:
        return render(request, 'student/dashboard.html', {
            'error': 'An error occurred while loading your dashboard.',
            'attendance': [],
            'result': None,
            'messages': [],
            'timetable': [],
            'courses': []
        })