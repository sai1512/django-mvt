# Student Management Platform — Phase 1

## Overview

Build a Django web application that displays and manages student information. This is the **starting point of your final project** — we'll keep building on this throughout the course.

For now, all data is **hardcoded** in your views (lists of dictionaries). Tomorrow we'll replace this with a real database.

---

## Setup

```bash
# Create project folder and virtual environment
mkdir studentplatform && cd studentplatform
python -m venv venv
source venv/bin/activate        # Mac/Linux
# .\venv\Scripts\activate       # Windows

# Install Django
pip install django

# Create the project (the dot creates it in the current folder)
django-admin startproject studentplatform .

# Create the core app
python manage.py startapp core

# Run the dev server
python manage.py runserver
```

Don't forget to add `'core'` to `INSTALLED_APPS` in `settings.py`.

---

## Requirements

### Pages to build

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Welcome message with navigation |
| About | `/about/` | Course information |
| Students list | `/students/` | Table of all students |
| Student detail | `/students/<id>/` | Full details for one student |
| Add student | `/students/add/` | Form to add a new student |

### Technical requirements

1. **Project structure**
   - Django project called `studentplatform`
   - App called `core`
   - `core/urls.py` with all routes (included from the project `urls.py`)

2. **Views** (`core/views.py`)
   - Use the hardcoded `STUDENTS` list below as your data source
   - Each view uses `render()` to return a template with context data
   - The add student view handles both GET (show form) and POST (process form)
   - The detail view returns a 404 if the student ID doesn't exist

3. **Templates** (`core/templates/`)
   - `base.html` — shared layout with nav bar, CSS link, `{% block title %}` and `{% block content %}`
   - `home.html` — extends base, welcome message
   - `about.html` — extends base, course info
   - `student_list.html` — extends base, students in a `<table>` with links to detail pages
   - `student_detail.html` — extends base, shows all fields for one student
   - `add_student.html` — extends base, form with `{% csrf_token %}`

4. **Static files** (`core/static/css/style.css`)
   - Basic styling: fonts, table formatting, nav bar, form styling
   - Loaded in `base.html` with `{% load static %}`

5. **Navigation**
   - Every page has a nav bar (from `base.html`) with links to Home, Students, Add Student
   - Use `{% url 'name' %}` for all links — no hardcoded paths

---

## Student Data

Use this at the top of `views.py`:

```python
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
```

---

## File structure

When you're done, your project should look like this:

```
studentplatform/
├── manage.py
├── studentplatform/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── core/
    ├── urls.py              ← you create this
    ├── views.py
    ├── templates/
    │   ├── base.html
    │   ├── home.html
    │   ├── about.html
    │   ├── student_list.html
    │   ├── student_detail.html
    │   └── add_student.html
    └── static/
        └── css/
            └── style.css
```

---

## Hints

- **Template inheritance**: `base.html` contains everything shared (doctype, head, nav, footer). Child templates use `{% extends 'base.html' %}` and fill in `{% block content %}`.

- **Linking to detail pages**: In `student_list.html`, use:
  ```html
  <a href="{% url 'student_detail' student.id %}">{{ student.name }}</a>
  ```

- **Finding a student by ID**: In the detail view, loop through `STUDENTS` to find the one with the matching `id`. Return a 404 if not found:
  ```python
  from django.http import HttpResponse

  def student_detail(request, student_id):
      student = None
      for s in STUDENTS:
          if s["id"] == student_id:
              student = s
      if student is None:
          return HttpResponse("Student not found", status=404)
      return render(request, "student_detail.html", {"student": student})
  ```

- **Handling the add form**: The same view handles GET (show the form) and POST (process it):
  ```python
  from django.shortcuts import render, redirect

  def add_student(request):
      if request.method == "POST":
          STUDENTS.append({
              "id": len(STUDENTS) + 1,
              "name": request.POST.get("name"),
              "email": request.POST.get("email"),
              "course": request.POST.get("course"),
              "grade": request.POST.get("grade"),
          })
          return redirect("student_list")
      return render(request, "add_student.html")
  ```

- **CSRF token**: Every `<form method="POST">` needs `{% csrf_token %}` inside it, or Django will reject the submission.

- **Data won't persist**: Since we're using a Python list, added students disappear when you restart the server. That's expected — tomorrow we add a database.

---

## Bonus challenges

- [ ] **Delete student**: Add a delete button/link on the detail page that removes a student
- [ ] **Edit student**: Create an edit form pre-filled with existing data that updates on submit
- [ ] **Search**: Add a search box on the student list that filters by name
- [ ] **Student count**: Show the total number of students in the nav bar or list page header
- [ ] **Styling**: Make it look good — add colors, spacing, hover effects on the table rows
