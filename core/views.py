from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.http import HttpResponseForbidden

from .models import Course, Student




def home(request):
    """Home page — welcome message."""
    # TODO: render home.html
    return render(request, 'home.html')


def about(request):
    """About page — course information."""
    # TODO: render about.html
    return render(request, 'about.html')

@login_required
def student_list(request):
    selected_course_id = request.GET.get('course')
    # students = Student.objects.select_related('course').order_by('name')
    if request.user.is_staff:
        students = Student.objects.select_related('course').order_by('name')
    else:
        students = Student.objects.select_related('course').filter(created_by=request.user).order_by('name')
    selected_course = None

    if selected_course_id and selected_course_id.isdigit():
        students = students.filter(course_id=selected_course_id)
        selected_course = Course.objects.filter(id=selected_course_id).first()

    # courses = Course.objects.annotate(student_count=Count('students')).order_by('name')
    if request.user.is_staff:
        courses = Course.objects.annotate(student_count=Count('students')).order_by('name')
    else:
        courses = Course.objects.annotate(student_count=Count('students', filter=Q(students__created_by=request.user))).order_by('name')
    content = {
        'students': students,
        'total_students': students.count(),
        'courses': courses,
        'selected_course': selected_course,
    }
    return render(request, 'student_list.html', content)

@login_required
def student_detail(request, student_id):
    """Show details for a single student."""
    # student = get_object_or_404(Student.objects.select_related('course'), id=student_id)
    if request.user.is_staff:
        student = get_object_or_404(Student.objects.select_related('course'), id=student_id)
    else:
        student = get_object_or_404(Student.objects.select_related('course'), id=student_id, created_by=request.user)
    return render(request, 'student_detail.html', {'student': student})

@login_required
def add_student(request):
    """Show a form (GET) or process the submission (POST)."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth') or None
        grade = request.POST.get('grade')
        course_id = request.POST.get('course_id')

        
        Student.objects.create(
            name=name,
            email=email,
            date_of_birth=date_of_birth,
            grade=grade,
            course_id=course_id,
            created_by=request.user,
        )

        return redirect('student_list')

    courses = Course.objects.order_by('name')
    return render(request, 'add_student.html', {'courses': courses})

@login_required
def edit_student(request, student_id):
    if not request.user.is_staff:
        return HttpResponseForbidden('Only admin users can edit students.')

    # student = get_object_or_404(Student, id=student_id, created_by=request.user)
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.name = request.POST.get('name')
        student.email = request.POST.get('email')
        student.date_of_birth = request.POST.get('date_of_birth') or None
        student.grade = request.POST.get('grade')
        student.is_active = request.POST.get('is_active') == 'on'
        student.course_id = request.POST.get('course_id')
        student.save()
        return redirect('student_detail', student_id=student.id)

    courses = Course.objects.order_by('name')
    return render(request, 'edit_student.html', {'student': student, 'courses': courses})

@login_required
def delete_student(request, student_id):
    if not request.user.is_staff:
        return HttpResponseForbidden('Only admin users can delete students.')

    # student = get_object_or_404(Student, id=student_id, created_by=request.user)
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('student_list')

@login_required
def course_list(request):
    courses = Course.objects.annotate(student_count=Count('students')).order_by('name')
    return render(request, 'course_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # students = course.students.select_related('course').order_by('name')
    if request.user.is_staff:
        students = course.students.select_related('course').order_by('name')
    else:
        students = course.students.select_related('course').filter(created_by=request.user).order_by('name')
    return render(request, 'course_detail.html', {'course': course, 'students': students})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_list')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
        
    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        email = (request.POST.get('email') or '').strip()
        password = request.POST.get('password') or ''
        confirm_password = request.POST.get('confirm_password') or ''

        if not username or not password:
            return render(request, 'signup.html', {'error': 'Username and password are required.'})

        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists.'})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('student_list')

    return render(request, 'signup.html')


@login_required
def change_password_view(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password') or ''
        new_password = request.POST.get('new_password') or ''
        confirm_password = request.POST.get('confirm_password') or ''

        if not request.user.check_password(current_password):
            return render(request, 'change_password.html', {'error': 'Current password is incorrect.'})

        if new_password != confirm_password:
            return render(request, 'change_password.html', {'error': 'New passwords do not match.'})

        try:
            validate_password(new_password, user=request.user)
        except ValidationError as exc:
            return render(request, 'change_password.html', {'error': ' '.join(exc.messages)})

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        return render(request, 'change_password.html', {'success': 'Password changed successfully.'})

    return render(request, 'change_password.html')


def logout_view(request):
    logout(request)
    return redirect('home')
