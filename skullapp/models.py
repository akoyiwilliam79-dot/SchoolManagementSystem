from django.db import models
from django.shortcuts import render, redirect, get_object_or_404

# Create your models here.


# -----------------
# STUDENT MODEL
# -----------------
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=20, unique=True)
    student_class = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# -----------------
# TEACHER MODEL
# -----------------
class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    

def teachers(request):
    teachers = Teacher.objects.all()
    return render(request, 'teachers.html', {'teachers': teachers})


def add_teacher(request):
    if request.method == "POST":
        name = request.POST['name']
        subject = request.POST['subject']
        phone = request.POST['phone']

        Teacher.objects.create(
            name=name,
            subject=subject,
            phone=phone
        )
        return redirect('teachers')

    return render(request, 'add_teacher.html')

def edit_teacher(request, pk):
    teacher = get_object_or_404(Teacher, id=pk)

    if request.method == "POST":
        teacher.name = request.POST['name']
        teacher.subject = request.POST['subject']
        teacher.phone = request.POST['phone']
        teacher.save()

        return redirect('teachers')

    return render(request, 'edit_teacher.html', {'teacher': teacher})
def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, id=pk)

    if request.method == "POST":
        teacher.delete()
        return redirect('teachers')

    return render(request, 'delete_teacher.html', {'teacher': teacher})


## -----------------
# SIMPLE FEE MODEL (CLEAN)
# -----------------
class Fee(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    amount_paid = models.IntegerField(default=0)
    total_fee = models.IntegerField(default=0)
    @property
    def balance(self):
        return self.total_fee - self.amount_paid

    def __str__(self):
        return f"{self.student.first_name} - {self.amount_paid}"
# -----------------
# ATTENDANCE MODEL
# -----------------
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[
        ('Present', 'Present'),
        ('Absent', 'Absent')
    ])

    def __str__(self):
        return f"{self.student.first_name} - {self.status}"


# -----------------
# RESULTS MODEL
# -----------------
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    english = models.IntegerField(default=0)
    kiswahili = models.IntegerField(default=0)
    maths = models.IntegerField(default=0)
    science = models.IntegerField(default=0)
    social_studies = models.IntegerField(default=0)
    cre = models.IntegerField(default=0)
    computer = models.IntegerField(default=0)
    business = models.IntegerField(default=0)
    agriculture = models.IntegerField(default=0)

    def total(self):
        return (
            self.english +
            self.kiswahili +
            self.maths +
            self.science +
            self.social_studies +
            self.cre +
            self.computer +
            self.business +
            self.agriculture
        )

    def __str__(self):
        return f"{self.student.first_name} - {self.total()}"
    

def results(request):
    results = Result.objects.all()
    return render(request, 'results.html', {'results': results})
def add_result(request):
    students = Student.objects.all()

    if request.method == "POST":
        Result.objects.create(
            student_id=request.POST['student'],
            english=request.POST['english'],
            kiswahili=request.POST['kiswahili'],
            maths=request.POST['maths'],
            science=request.POST['science'],
            social_studies=request.POST['social_studies'],
            cre=request.POST['cre'],
            computer=request.POST['computer'],
            business=request.POST['business'],
            agriculture=request.POST['agriculture'],
        )
        return redirect('results')

    return render(request, 'add_result.html', {'students': students})
def edit_result(request, pk):
    result = get_object_or_404(Result, id=pk)
    students = Student.objects.all()

    if request.method == "POST":
        result.student_id = request.POST['student']
        result.english = request.POST['english']
        result.kiswahili = request.POST['kiswahili']
        result.maths = request.POST['maths']
        result.science = request.POST['science']
        result.social_studies = request.POST['social_studies']
        result.cre = request.POST['cre']
        result.computer = request.POST['computer']
        result.business = request.POST['business']
        result.agriculture = request.POST['agriculture']
        result.save()

        return redirect('results')

    return render(request, 'edit_result.html', {
        'result': result,
        'students': students
    })

def delete_result(request, pk):
    result = get_object_or_404(Result, id=pk)

    if request.method == "POST":
        result.delete()
        return redirect('results')

    return render(request, 'delete_result.html', {'result': result})
