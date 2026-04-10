from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/', views.students, name='students'),
    path('teachers/', views.teachers, name='teachers'),
    path('fees/', views.fees, name='fees'),
    path('attendance/', views.attendance, name='attendance'),
    path('results/', views.results, name='results'),
    path('base/', views.base, name='base'),
    path('add/', views.add_student, name='add_student'),
]