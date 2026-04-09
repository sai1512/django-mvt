from django.contrib import admin
from .models import Course, Student


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ('code', 'name', 'description')
	search_fields = ('code', 'name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'grade', 'is_active', 'course', 'created_at')
	list_filter = ('is_active', 'course')
	search_fields = ('name', 'email')

