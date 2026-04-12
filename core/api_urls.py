from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .api_views import (
    CourseStudentsListAPIView,
    StudentListCreateAPIView,
    StudentRetrieveUpdateDestroyAPIView,
    CourseListCreateAPIView,
    CourseRetrieveUpdateDestroyAPIView
)

urlpatterns = [

    # JWT Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    
    

    # API endpoints for Student model
    path('students/', StudentListCreateAPIView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentRetrieveUpdateDestroyAPIView.as_view(), name='student-retrieve-update-destroy'),

    # API endpoints for Course model
    path('courses/', CourseListCreateAPIView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyAPIView.as_view(), name='course-retrieve-update-destroy'),

    # Nested endpoint for listing students in a specific course
    path('courses/<int:pk>/students/', CourseStudentsListAPIView.as_view(), name='course-students-list'),
]