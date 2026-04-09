from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404

from .models import Course, Student




def home(request):
    """Home page — welcome message."""
    # TODO: render home.html
    return render(request, 'home.html')


def about(request):
    """About page — course information."""
    # TODO: render about.html
    return render(request, 'about.html')


def student_list(request):
    selected_course_id = request.GET.get('course')
    students = Student.objects.select_related('course').order_by('name')
    selected_course = None

    if selected_course_id and selected_course_id.isdigit():
        students = students.filter(course_id=selected_course_id)
        selected_course = Course.objects.filter(id=selected_course_id).first()

    courses = Course.objects.annotate(student_count=Count('students')).order_by('name')
    content = {
        'students': students,
        'total_students': students.count(),
        'courses': courses,
        'selected_course': selected_course,
    }
    return render(request, 'student_list.html', content)


def student_detail(request, student_id):
    """Show details for a single student."""
    student = get_object_or_404(Student.objects.select_related('course'), id=student_id)
    return render(request, 'student_detail.html', {'student': student})


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
        )

        return redirect('student_list')

    courses = Course.objects.order_by('name')
    return render(request, 'add_student.html', {'courses': courses})


def edit_student(request, student_id):
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


def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('student_list')


def course_list(request):
    courses = Course.objects.annotate(student_count=Count('students')).order_by('name')
    return render(request, 'course_list.html', {'courses': courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = course.students.select_related('course').order_by('name')
    return render(request, 'course_detail.html', {'course': course, 'students': students})