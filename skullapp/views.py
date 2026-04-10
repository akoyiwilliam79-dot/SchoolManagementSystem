from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def dashboard(request):
    students = Student.objects.count()
    teachers = Teacher.objects.count()
    fees = Fee.objects.all()

    total_collected = sum([f.amount_paid for f in fees])

    context = {
        'students': students,
        'teachers': teachers,
        'fees': total_collected
    }
    return render(request, 'dashboard.html', context)


def students(request):
    students = Student.objects.all()
    return render(request, 'students.html', {'students': students})


def teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers.html', {'teachers': teachers})


def fees(request):
    fees = Fee.objects.all()
    return render(request, 'fees.html', {'fees': fees})


def attendance(request):
    attendance = Attendance.objects.all()
    return render(request, 'attendance.html', {'attendance': attendance})


def results(request):
    results = Result.objects.all()
    return render(request, 'results.html', {'results': results})


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