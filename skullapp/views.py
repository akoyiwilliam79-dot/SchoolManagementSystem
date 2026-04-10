from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.db.models import Sum, Count
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



@login_required


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
def get_grade(mark):
    if mark >= 80:
        return "A", "green"
    elif mark >= 70:
        return "B", "blue"
    elif mark >= 60:
        return "C", "gold"
    elif mark >= 50:
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


def add_teacher(request):
    if request.method == "POST":
        name = request.POST.get('name')
        subject1 = request.POST.get('subject1')
        subject2 = request.POST.get('subject2')
        subject3 = request.POST.get('subject3')
        phone = request.POST.get('phone')

        Teacher.objects.create(
            name=name,
            subject1=subject1,
            subject2=subject2,
            subject3=subject3,
            phone=phone
        )

        return redirect('teachers')

    return render(request, 'skullapp/add_teacher.html')

@login_required
def fees(request):
    fees = Fee.objects.all()
    return render(request, 'fees.html', {'fees': fees})


@login_required
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



@login_required
def results(request):
    results = Result.objects.all()
    return render(request, 'results.html', {'results': results})

@login_required

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



#Login View

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # ONLY redirect here
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


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