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
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from .models import Attendance
from decimal import Decimal




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

@login_required
def students(request):
    return render(request, 'students.html')

from django.db.models import Q

def students(request):
    query = request.GET.get('q')

    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(student_class__icontains=query) |
            Q(admission_number__icontains=query)
        )

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
        'student_data': student_data,
        'query': query
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


def admin_only(user):
    return user.is_staff

@login_required
@user_passes_test(admin_only)
def fees(request):
    ...

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

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('students')

        messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'register.html')
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
            amount_paid = int(request.POST.get('amount_paid') or 0),
            total_fee = int(request.POST.get('total_fee') or 0),
        )
        return redirect('fees')

    return render(request, 'add_fee.html', {'students': students})


def edit_fee(request, pk):
    fee = get_object_or_404(Fee, id=pk)
    students = Student.objects.all()

    if request.method == "POST":
        fee.student_id = request.POST['student']
        fee.amount_paid = (request.POST.get('amount_paid') or 0)
        fee.total_fee = (request.POST.get('total_fee') or 0)
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

def add_results(request):
    if request.method == "POST":
        # your logic to save results here

        messages.success(request, "Results entered successfully!")
        messages.info(request, "Student records updated successfully!")

        return redirect('add_results')  # or wherever you want

    return render(request, 'add_results.html')

def delete_result(request, pk):
    result = Result.objects.get(id=pk)
    result.delete()

    messages.warning(request, "Result deleted successfully!")
    return redirect('results')


def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()

    messages.success(request, "Student deleted successfully!")
    return redirect('students')


def edit_attendance(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)

    if request.method == "POST":
        attendance.status = request.POST.get('status')
        attendance.date = request.POST.get('date')
        attendance.save()

        messages.success(request, "Attendance updated successfully!")
        return redirect('attendance')

    return render(request, 'edit_attendance.html', {'attendance': attendance})

def delete_attendance(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    attendance.delete()

    messages.success(request, "Attendance deleted successfully!")
    return redirect('attendance')