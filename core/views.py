"""
Session 3 — Student Management Platform (Phase 1)
core/views.py

Complete the views below. Each view should:
1. Prepare any data needed (from the STUDENTS list)
2. Return render() with the appropriate template and context
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse


# Hardcoded student data — tomorrow we'll replace this with a database
STUDENTS = [
    {
        "id": 1,
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "course": "Computer Science",
        "grade": "A",
    },
    {
        "id": 2,
        "name": "Alan Turing",
        "email": "alan@example.com",
        "course": "Mathematics",
        "grade": "A+",
    },
    {
        "id": 3,
        "name": "Grace Hopper",
        "email": "grace@example.com",
        "course": "Engineering",
        "grade": "B+",
    },
    {
        "id": 4,
        "name": "Linus Torvalds",
        "email": "linus@example.com",
        "course": "Operating Systems",
        "grade": "A",
    },
]


def home(request):
    """Home page — welcome message."""
    # TODO: render home.html
    return render(request, 'home.html')


def about(request):
    """About page — course information."""
    # TODO: render about.html
    return render(request, 'about.html')


def student_list(request):
    """List all students in a table."""
    # TODO: pass STUDENTS and the total count to student_list.html
    content = {
        'students' : STUDENTS,
        'total_students' : len(STUDENTS)
    }
    return render(request, 'student_list.html', content)


def student_detail(request, student_id):
    """Show details for a single student."""
    # TODO: find the student with matching id
    # if not found, return HttpResponse("Student not found", status=404)
    # if found, render student_detail.html with the student data
    student = None
    for s in STUDENTS:
        if s['id'] == student_id:
            student = s
            break
    if student is None:
        return HttpResponse("Student not found", status=404)
    return render(request, 'student_detail.html', {'student': student})


def add_student(request):
    """Show a form (GET) or process the submission (POST)."""
    # TODO: if POST, read form data from request.POST, append to STUDENTS, redirect
    # TODO: if GET, render add_student.html
    if request.method == 'POST':
        # Read form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        course = request.POST.get('course')
        grade = request.POST.get('grade')

        # Create new student dictionary
        new_student = {
            "id": len(STUDENTS) + 1,
            "name": name,
            "email": email,
            "course": course,
            "grade": grade
        }

        # Append to STUDENTS list
        STUDENTS.append(new_student)

        # Redirect to student list
        return redirect('student_list')
    else:
        return render(request, 'add_student.html')