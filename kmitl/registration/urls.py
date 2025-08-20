from django.urls import path

from . import views

urlpatterns = [
    
    path("student/", views.student_list, name="student-list"),
    path("professor/", views.professor_list, name="professor-list"),
    path("course/", views.course_list, name="course-list"),
    path("faculty/", views.faculty_list, name="faculty-list"),
    path('student/create/', views.create_student, name='create_student'),
    path('student/', views.student_list, name='student_list'),
]