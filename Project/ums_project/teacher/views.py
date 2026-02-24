from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from student.models import Attendance, Course, Result, Message, Timetable
from accounts.models import CustomUser


def teacher_required(view_func):
    """Decorator to check if user is a teacher"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.user_type != 'teacher':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('student_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@teacher_required
def teacher_dashboard(request):
  
    total_students = CustomUser.objects.filter(user_type='student').count()
    total_courses = Course.objects.count()
    total_attendances = Attendance.objects.count()
    
    return render(request, 'teacher/dashboard.html', {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_attendances': total_attendances,
    })


@login_required
@teacher_required
def mark_attendance(request):
    students = CustomUser.objects.filter(user_type='student')
    courses = Course.objects.all()

    if request.method == "POST":
        try:
            student_id = request.POST.get('student')
            course_id = request.POST.get('course')
            present = request.POST.get('present')

            if not student_id or not course_id:
                messages.error(request, 'Student and course are required.')
                return redirect('mark_attendance')

            student = CustomUser.objects.get(id=student_id)
            course = Course.objects.get(id=course_id)

            attendance, created = Attendance.objects.get_or_create(
                student=student,
                course=course
            )

            attendance.total_classes += 1

            if present == "yes":
                attendance.attended_classes += 1

            attendance.save()
            messages.success(request, 'Attendance marked successfully.')
            return redirect('teacher_dashboard')
        except (CustomUser.DoesNotExist, Course.DoesNotExist):
            messages.error(request, 'Student or course not found.')
            return redirect('mark_attendance')

    return render(request, 'teacher/mark_attendance.html', {
        'students': students,
        'courses': courses
    })


@login_required
@teacher_required
def upload_cgpa(request):
    students = CustomUser.objects.filter(user_type='student')

    if request.method == "POST":
        try:
            student_id = request.POST.get('student')
            cgpa_value = request.POST.get('cgpa')

            if not student_id or not cgpa_value:
                messages.error(request, 'Student and CGPA are required.')
                return redirect('upload_cgpa')

            try:
                cgpa_float = float(cgpa_value)
                if cgpa_float < 0 or cgpa_float > 4.0:
                    messages.error(request, 'CGPA must be between 0 and 4.0.')
                    return redirect('upload_cgpa')
            except ValueError:
                messages.error(request, 'CGPA must be a valid number.')
                return redirect('upload_cgpa')

            student = CustomUser.objects.get(id=student_id)

            result, created = Result.objects.get_or_create(student=student)
            result.cgpa = cgpa_float  # Store as float
            result.save()

            messages.success(request, 'CGPA uploaded successfully.')
            return redirect('teacher_dashboard')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Student not found.')
            return redirect('upload_cgpa')

    return render(request, 'teacher/upload_cgpa.html', {
        'students': students
    })


@login_required
@teacher_required
def send_message(request):
    students = CustomUser.objects.filter(user_type='student')

    if request.method == "POST":
        try:
            student_id = request.POST.get('student')
            content = request.POST.get('content')

            if not student_id or not content:
                messages.error(request, 'Student and message content are required.')
                return redirect('send_message')

            if len(content.strip()) == 0:
                messages.error(request, 'Message cannot be empty.')
                return redirect('send_message')

            student = CustomUser.objects.get(id=student_id)

            Message.objects.create(
                sender=request.user,
                receiver=student,
                content=content
            )

            messages.success(request, 'Message sent successfully.')
            return redirect('teacher_dashboard')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Student not found.')
            return redirect('send_message')

    return render(request, 'teacher/send_message.html', {
        'students': students
    })


@login_required
@teacher_required
def add_timetable(request):
    courses = Course.objects.all()

    if request.method == "POST":
        try:
            course_id = request.POST.get('course')
            day = request.POST.get('day')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            room = request.POST.get('room')

            if not all([course_id, day, start_time, end_time, room]):
                messages.error(request, 'All fields are required.')
                return redirect('add_timetable')

            course = Course.objects.get(id=course_id)

            # Validate that end_time is after start_time
            if start_time >= end_time:
                messages.error(request, 'End time must be after start time.')
                return redirect('add_timetable')

            Timetable.objects.create(
                course=course,
                day=day,
                start_time=start_time,
                end_time=end_time,
                room=room
            )

            messages.success(request, 'Timetable added successfully.')
            return redirect('teacher_dashboard')
        except Course.DoesNotExist:
            messages.error(request, 'Course not found.')
            return redirect('add_timetable')

    return render(request, 'teacher/add_timetable.html', {
        'courses': courses
    })


@login_required
@teacher_required
def manage_courses(request):
    """View to list all courses"""
    courses = Course.objects.all().order_by('semester', 'name')
    
    return render(request, 'teacher/manage_courses.html', {
        'courses': courses
    })


@login_required
@teacher_required
def add_course(request):
    """View to add a new course"""
    if request.method == "POST":
        try:
            course_name = request.POST.get('name')
            semester = request.POST.get('semester')

            if not course_name or not semester:
                messages.error(request, 'Course name and semester are required.')
                return redirect('add_course')

            try:
                semester_int = int(semester)
                if semester_int < 1 or semester_int > 8:
                    messages.error(request, 'Semester must be between 1 and 8.')
                    return redirect('add_course')
            except ValueError:
                messages.error(request, 'Semester must be a valid number.')
                return redirect('add_course')

            # Check if course already exists
            if Course.objects.filter(name__iexact=course_name).exists():
                messages.error(request, f'Course "{course_name}" already exists.')
                return redirect('add_course')

            Course.objects.create(
                name=course_name,
                semester=semester_int
            )

            messages.success(request, f'Course "{course_name}" added successfully.')
            return redirect('manage_courses')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('add_course')

    return render(request, 'teacher/add_course.html')


@login_required
@teacher_required
def edit_course(request, course_id):
    """View to edit a course"""
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
        return redirect('manage_courses')

    if request.method == "POST":
        try:
            course_name = request.POST.get('name')
            semester = request.POST.get('semester')

            if not course_name or not semester:
                messages.error(request, 'Course name and semester are required.')
                return redirect('edit_course', course_id=course_id)

            try:
                semester_int = int(semester)
                if semester_int < 1 or semester_int > 8:
                    messages.error(request, 'Semester must be between 1 and 8.')
                    return redirect('edit_course', course_id=course_id)
            except ValueError:
                messages.error(request, 'Semester must be a valid number.')
                return redirect('edit_course', course_id=course_id)

            # Check if another course with this name exists
            if Course.objects.filter(name__iexact=course_name).exclude(id=course_id).exists():
                messages.error(request, f'Course "{course_name}" already exists.')
                return redirect('edit_course', course_id=course_id)

            course.name = course_name
            course.semester = semester_int
            course.save()

            messages.success(request, f'Course "{course_name}" updated successfully.')
            return redirect('manage_courses')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('edit_course', course_id=course_id)

    return render(request, 'teacher/edit_course.html', {'course': course})


@login_required
@teacher_required
def delete_course(request, course_id):
    """View to delete a course"""
    try:
        course = Course.objects.get(id=course_id)
        course_name = course.name
        
    
        if Attendance.objects.filter(course=course).exists():
            messages.error(request, f'Cannot delete course "{course_name}" - it has attendance records.')
            return redirect('manage_courses')
        
        if Timetable.objects.filter(course=course).exists():
            messages.error(request, f'Cannot delete course "{course_name}" - it has timetable entries.')
            return redirect('manage_courses')
        
        course.delete()
        messages.success(request, f'Course "{course_name}" deleted successfully.')
        return redirect('manage_courses')
    except Course.DoesNotExist:
        messages.error(request, 'Course not found.')
        return redirect('manage_courses')