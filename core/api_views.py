from rest_framework import generics, filters
from django.db.models import Q
from .models import Student, Course
from .serializers import StudentSerializer, CourseSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

# API Views for Student model

#class StudentListCreateAPIView(generics.ListCreateAPIView):
#    queryset = Student.objects.select_related('course').all()
#    serializer_class = StudentSerializer

class StudentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']


    def get_queryset(self):
        # queryset = Student.objects.select_related("course").all()
        if self.request.user.is_staff:
            queryset = Student.objects.select_related("course").all()
        else:
            queryset = Student.objects.select_related("course").filter(created_by=self.request.user)

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

    def perform_create(self, serializer):
        # Automatically set created_by to the current user
        serializer.save(created_by=self.request.user)

class StudentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    # queryset = Student.objects.select_related('course').all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter to only show students created by the current user
        # return Student.objects.select_related('course').filter(created_by=self.request.user)
        if self.request.user.is_staff:
            return Student.objects.select_related('course').all()
        return Student.objects.select_related('course').filter(created_by=self.request.user)


# API Views for Course model

class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

# Nested endpoint

class CourseStudentsListAPIView(generics.ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs["pk"])
        # return course.students.select_related("course").all()
        if self.request.user.is_staff:
            return course.students.select_related("course").all()
        return course.students.select_related("course").filter(created_by=self.request.user)
    

