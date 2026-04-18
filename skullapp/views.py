from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.db.models import Sum, Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import requests
import base64
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import logout
from django.shortcuts import redirect
import requests, base64
from datetime import datetime
from django.conf import settings
from django.shortcuts import redirect
from .models import Fee








def dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()

    total_fees_collected = Fee.objects.aggregate(
        total=Sum('amount_paid')
    )['total'] or 0

    total_attendance = Attendance.objects.count()

    results_count = Result.objects.count()

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_fees_collected': total_fees_collected,
        'total_attendance': total_attendance,
        'results_count': results_count,
    }

    return render(request, 'dashboard.html', context)



def students(request):
    students = Student.objects.all()
    results = Result.objects.all()

    student_data = []

    for s in students:
        result = results.filter(student=s).first()

        grade = None
        color = None

        if result:
            grade, color = get_grade(result.total())

        student_data.append({
            'student': s,
            'result': result,
            'grade': grade,
            'color': color
        })

    return render(request, 'students.html', {
        'student_data': student_data
    })


#grade function
def get_grade(total):
    if total >= 700:
        return "A", "green"
    elif total >= 600:
        return "B", "blue"
    elif total >= 500:
        return "C", "gold"
    elif total >= 400:
        return "D", "orange"
    else:
        return "E", "red"

def edit_student(request, pk):
    student = get_object_or_404(Student, id=pk)

    if request.method == "POST":
        student.first_name = request.POST['first_name']
        student.last_name = request.POST['last_name']
        student.admission_number = request.POST['admission_number']
        student.student_class = request.POST['student_class']
        student.save()

        return redirect('students')

    return render(request, 'edit_student.html', {'student': student})

def delete_student(request, pk):
    student = get_object_or_404(Student, id=pk)

    if request.method == "POST":
        student.delete()
        return redirect('students')

    return render(request, 'delete_student.html', {'student': student})


def teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers.html', {'teachers': teachers})


def fees(request):
    fees = Fee.objects.all()
    return render(request, 'fees.html', {'fees': fees})



def attendance(request):
    attendance_records = Attendance.objects.all().order_by('-date')
    students = Student.objects.all()

    return render(request, 'attendance.html', {
        'attendance': attendance_records,
        'students': students
    })

def mark_attendance(request):
    if request.method == "POST":
        student_id = request.POST['student']
        date = request.POST['date']
        status = request.POST['status']

        Attendance.objects.create(
            student_id=student_id,
            date=date,
            status=status
        )

        return redirect('attendance')

    return redirect('attendance')




def results(request):
    results = Result.objects.all()
    return render(request, 'results.html', {'results': results})



def student_results(request):
    results = Result.objects.filter(student__user=request.user)
    return render(request, 'student_results.html', {'results': results})


def base(request):
    return render(request, 'base.html', {'base': base})


def add_student(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        admission_number = request.POST['admission_number']
        student_class = request.POST['student_class']

        # CHECK IF EXISTS FIRST
        if Student.objects.filter(admission_number=admission_number).exists():
            messages.error(request, "Admission number already exists!")
            return redirect('add_student')

        Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            admission_number=admission_number,
            student_class=student_class
        )

        messages.success(request, "Student added successfully!")
        return redirect('students')

    return render(request, 'add_student.html')





#User role

def user_role(user):
    if user.groups.filter(name='Admin').exists():
        return 'admin'
    elif user.groups.filter(name='Teacher').exists():
        return 'teacher'
    elif user.groups.filter(name='Student').exists():
        return 'student'
    return 'none'


def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Admin').exists():
            return view_func(request, *args, **kwargs)
        return HttpResponse("Access Denied: Admins only")
    return wrapper

def teacher_or_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name__in=['Admin', 'Teacher']).exists():
            return view_func(request, *args, **kwargs)
        return HttpResponse("Access Denied")
    return wrapper

def student_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.groups.filter(name='Student').exists():
            return view_func(request, *args, **kwargs)
        return HttpResponse("Access Denied")
    return wrapper




def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')  # or dashboard
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')





def fees(request):
    fees = Fee.objects.all()
    return render(request, 'fees.html', {'fees': fees})


def add_fee(request):
    students = Student.objects.all()

    if request.method == "POST":
        Fee.objects.create(
            student_id=request.POST['student'],
            amount_paid=request.POST['amount_paid'],
            total_fee=request.POST['total_fee']
        )
        return redirect('fees')

    return render(request, 'add_fee.html', {'students': students})


def edit_fee(request, pk):
    fee = get_object_or_404(Fee, id=pk)
    students = Student.objects.all()

    if request.method == "POST":
        fee.student_id = request.POST['student']
        fee.amount_paid = request.POST['amount_paid']
        fee.total_fee = request.POST['total_fee']
        fee.save()
        return redirect('fees')

    return render(request, 'edit_fee.html', {'fee': fee, 'students': students})


def delete_fee(request, pk):
    fee = get_object_or_404(Fee, id=pk)

    if request.method == "POST":
        fee.delete()
        return redirect('fees')

    return render(request, 'delete_fee.html', {'fee': fee})


def edit_result(request, pk):
    result = get_object_or_404(Result, id=pk)

    if request.method == "POST":
        result.english = request.POST.get('english')
        result.kiswahili = request.POST.get('kiswahili')
        result.maths = request.POST.get('maths')
        result.science = request.POST.get('science')
        result.social_studies = request.POST.get('social_studies')
        result.cre = request.POST.get('cre')
        result.computer = request.POST.get('computer')
        result.business = request.POST.get('business')
        result.agriculture = request.POST.get('agriculture')

        result.save()

        return redirect('results')

    # IMPORTANT: this must always run for GET requests
    return render(request, 'edit_result.html', {
        'result': result
    })

