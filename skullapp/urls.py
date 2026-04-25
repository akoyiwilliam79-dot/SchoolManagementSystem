from django.urls import path
from . import views

urlpatterns = [
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('students/', views.students, name='students'),
    path('teachers/', views.teachers, name='teachers'),
    path('fees/', views.fees, name='fees'),
    path('attendance/', views.attendance, name='attendance'),
    path('results/', views.results, name='results'),
    path('base/', views.base, name='base'),
    path('add/', views.add_student, name='add_student'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/edit/<int:pk>/', views.edit_attendance, name='edit_attendance'),
    path('attendance/delete/<int:pk>/', views.delete_attendance, name='delete_attendance'),
    path('students/edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('teachers/edit/<int:pk>/', views.edit_teacher, name='edit_teacher'),
    path('teachers/delete/<int:pk>/', views.delete_teacher, name='delete_teacher'),
    path('fees/add/', views.add_fee, name='add_fee'),
    path('fees/edit/<int:pk>/', views.edit_fee, name='edit_fee'),
    path('fees/delete/<int:pk>/', views.delete_fee, name='delete_fee'),
    path('results/add/', views.add_result, name='add_result'),
    path('results/edit/<int:pk>/', views.edit_result, name='edit_result'),
    path('results/delete/<int:pk>/', views.delete_result, name='delete_result'),
    path('student_results/', views.student_results, name='student_results'),
    path('login/', views.user_login, name='login'),
    path('', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
   

]
    
