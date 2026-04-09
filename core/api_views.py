from rest_framework import generics, filters
from .models import Student, Course
from .serializers import StudentSerializer, CourseSerializer
from django.shortcuts import get_object_or_404

# API Views for Student model

#class StudentListCreateAPIView(generics.ListCreateAPIView):
#    queryset = Student.objects.select_related('course').all()
#    serializer_class = StudentSerializer

class StudentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StudentSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']


    def get_queryset(self):
        queryset = Student.objects.select_related("course").all()

        grade = self.request.query_params.get("grade")
        if grade:
            queryset = queryset.filter(grade=grade)

        is_active = self.request.query_params.get("is_active")
        if is_active is not None:
            value = is_active.lower()
            if value in ("true", "1"):
                queryset = queryset.filter(is_active=True)
            elif value in ("false", "0"):
                queryset = queryset.filter(is_active=False)

        return queryset

class StudentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.select_related('course').all()
    serializer_class = StudentSerializer

# API Views for Course model

class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# Nested endpoint — add /api/courses/<pk>/students/ using ListAPIView with a filtered queryset

class CourseStudentsListAPIView(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs["pk"])
        return course.students.select_related("course").all()
    

