from django.db import models

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


# -----------------
# FEES MODEL
# -----------------
class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def balance(self):
        return self.total_fee - self.amount_paid

    def __str__(self):
        return f"{self.student.first_name} - Paid: {self.amount_paid}"

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
    subject = models.CharField(max_length=100)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.student.first_name} - {self.subject}: {self.score}"