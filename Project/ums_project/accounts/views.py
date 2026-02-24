from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Reg validation
            if user.user_type == 'student' and len(user.reg_no) != 7:
                user.delete()
                form.add_error('reg_no', 'Student Reg No must be 7 digits')
                return render(request, 'accounts/register.html', {'form': form})

            elif user.user_type == 'teacher' and len(user.reg_no) != 5:
                user.delete()
                form.add_error('reg_no', 'Teacher Reg No must be 5 digits')
                return render(request, 'accounts/register.html', {'form': form})

            else:
                messages.success(request, "Account created successfully. You are ready to login.")
                return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard_redirect(request):
    if request.user.user_type == 'student':
        return redirect('student_dashboard')
    else:
        return redirect('teacher_dashboard')


@login_required
def logout_view(request):
    logout(request)
    # Clear any messages from the session to prevent them from showing on login page
    from django.contrib.messages import constants as messages_constants
    storage = messages.get_messages(request)
    storage.used = True
    return redirect('login')