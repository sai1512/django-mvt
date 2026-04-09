# Student Management Platform — Phase 3

## Overview

Add a **REST API** to your student platform using Django REST Framework. Your app will serve both HTML pages (for browsers) and JSON data (for other software).

---

## What Changes From Yesterday

| Yesterday (Phase 2) | Today (Phase 3) |
|---|---|
| Data only accessible via HTML pages | Data also accessible via JSON API |
| No API endpoints | Full CRUD API for students and courses |

---

## Setup

```bash
pip install djangorestframework
```

Add to `settings.py`:
```python
INSTALLED_APPS = [
    ...,
    'rest_framework',
]
```

---

## Files to Create

You need **three new files** in your `core/` folder. Use the boilerplate from this repo as your starting point.

| New File | Purpose |
|---|---|
| `core/serializers.py` | Converts models to JSON and validates input |
| `core/api_views.py` | Handles API requests using DRF generic views |
| `core/api_urls.py` | Maps URL patterns to API views |

Then add this line to `studentplatform/urls.py`:
```python
path('api/', include('core.api_urls')),
```

---

## Requirements

### Serializers
- Create a `StudentSerializer` using `ModelSerializer`
- Create a `CourseSerializer` using `ModelSerializer`
- Use `fields = '__all__'` to include all model fields

### API Views
For each model you need two views using DRF generics:
- `ListCreateAPIView` — handles GET (list) and POST (create)
- `RetrieveUpdateDestroyAPIView` — handles GET (one), PUT, PATCH, DELETE

### API URLs
Wire up your views with `path()`:
- `/api/students/` → list + create
- `/api/students/<int:pk>/` → retrieve + update + delete
- `/api/courses/` → list + create
- `/api/courses/<int:pk>/` → retrieve + update + delete

Remember: DRF uses `pk` (primary key) in URL patterns, not `student_id`.

### Testing
Once everything is wired up:
1. Visit http://127.0.0.1:8000/api/students/ in your browser — you should see the browsable API
2. Try creating a student through the browsable API form
3. Try curl from the terminal:
   ```bash
   curl http://127.0.0.1:8000/api/students/
   curl http://127.0.0.1:8000/api/students/1/
   curl -X POST http://127.0.0.1:8000/api/students/ \
     -H "Content-Type: application/json" \
     -d '{"name":"Test","email":"test@test.com","grade":"A","course":1}'
   curl -X DELETE http://127.0.0.1:8000/api/students/1/
   ```

---

## Bonus Challenges

- [ ] **Nested endpoint** — add `/api/courses/<pk>/students/` using `ListAPIView` with a filtered queryset
- [ ] **Filtering** — filter students by grade or active status via query parameters
- [ ] **Search** — search students by name or email
- [ ] **Pagination** — configure DRF to paginate list responses

---

## When You're Done

```bash
pip freeze > requirements.txt
git add .
git commit -m "Session 5: REST API with DRF, serializers, generic views"
git push
```

**Tomorrow**: Authentication, security, encoding, and encryption.