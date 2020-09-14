from django.db import models
from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
import math
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils import timezone
import django
date_today = timezone.now()

test_name=(
    ('Insem','Insem'),
    ('Term Work','Term Work')
)

class User(AbstractUser):
    @property
    def is_teacher(self):
        if hasattr(self,'staff'):
            return True
        else:
            return False
    @property
    def is_student(self):
        if hasattr(self,'student'):
            return True
        else:
            return False

class Dept(models.Model):
    id = models.CharField(primary_key=True,max_length=50)
    name= models.CharField(max_length=50)
    def __str__(self):
        return '{}'.format(self.name)

class Batch(models.Model):
    id= models.CharField(primary_key=True,max_length=50)
    department = models.ForeignKey(Dept,on_delete=models.CASCADE)
    section = models.CharField(max_length=50)
    sem =models.IntegerField()

    def __str__(self):
        d = Dept.objects.get(name=self.department)
        return '{}:{}{}'.format(d.name,self.sem,self.section)

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    roll_no = models.CharField(primary_key=True,max_length=50)
    batch_id =models.ForeignKey(Batch,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    DOB =models.DateField()

    def __str__(self):
        return '{}'.format(self.name)

class Staff(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    id = models.CharField(primary_key=True,max_length=50)
    department =models.ForeignKey(Dept,on_delete=models.CASCADE)
    name =models.CharField(max_length=50)
    DOB = models.DateField()

    def __str__(self):
        return '{}'.format(self.name)

class Course(models.Model):
    id = models.CharField(primary_key=True,max_length=50)
    name = models.CharField(max_length=50)
    department = models.ForeignKey(Dept,on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)

class Teaches(models.Model):
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)

    class Meta:
        unique_together=['batch','course','staff']

    def __str__(self):
        btch = Batch.objects.get(id = self.batch_id)
        crs = Course.objects.get(id = self.course_id)
        stf = Staff.objects.get(id=self.staff_id)
        return '{}:{}'.format(btch,crs)

class Assignment(models.Model):
    teach = models.ForeignKey(Teaches,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    submission_date = models.DateField()
    doc = models.FileField(upload_to='assignments')

    def __str__(self):
        return '{}'.format(self.teach)

    @property
    def date_passed(self):
        return date.today() > self.submission_date

class PeriodTime(models.Model):
    TimeSlots = (
        ('8:45-9:45','8:45-9:45'),
        ('9:45-10:45', '9:45-10:45'),
        ('11:00-12:00', '11:00-12:00'),
        ('12:00-1:00', '12:00-1:00'),
        ('2:00-3:00', '2:00-3:00'),
    )
    DayOfWeek = (
        ('Monday','Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )
    teach = models.ForeignKey(Teaches,on_delete=models.CASCADE)
    period = models.CharField(max_length=50,choices=TimeSlots)
    day = models.CharField(max_length=20,choices=DayOfWeek)

    def __str__(self):
        return '{}:{}:{}'.format(self.teach,self.period,self.day)

class BatchAttendance(models.Model):
    teach = models.ForeignKey(Teaches,on_delete=models.CASCADE)
    date = models.DateField()
    status = models.IntegerField(default=0)

    def __str__(self):
        return '{} : {}'.format(self.teach,self.date)

class Attendance(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    batch_attendance= models.ForeignKey(BatchAttendance,on_delete=models.CASCADE)
    date = models.DateField(default=django.utils.timezone.now)
    status = models.BooleanField(default='True')

    def __str__(self):
        sname = Student.objects.get(name=self.student)
        cname = Course.objects.get(name=self.course)
        return '{} : {}'.format(sname.name,cname.name)

class AttendanceTotal(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)

    class Meta:
        unique_together = (('student','course'),)

    @property
    def attended_class(self):
        student = Student.objects.get(name=self.student)
        course=Course.objects.get(name=self.course)
        attendance_obj= Attendance.objects.filter(course=course,student=student,status='True').count()
        return attendance_obj

    @property
    def total_class(self):
        student = Student.objects.get(name=self.student)
        course = Course.objects.get(name=self.course)
        total_class=Attendance.objects.filter(course=course,student=student).count()
        return total_class

    @property
    def attendance(self):
        student = Student.objects.get(name=self.student)
        course = Course.objects.get(name=self.course)
        total_class = Attendance.objects.filter(course=course, student=student).count()
        att_class = Attendance.objects.filter(course=course, student=student,status='True').count()
        if total_class == 0:
            attd = 0
        else:
            attd = round(att_class/total_class *100,2)
        return attd

class StudentCourse(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    class Meta:
        unique_together=(('student','course'),)

    def __str__(self):
        return '{} : {}'.format(self.student,self.course)

class Marks(models.Model):
    student_course=models.ForeignKey(StudentCourse,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,choices=test_name)
    marks = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100)])

    class Meta:
        unique_together=(('student_course','name'),)

    def total_marks(self):
        if self.name=='Insem':
            return 30
        return 20

class MarksClass(models.Model):
    teach=models.ForeignKey(Teaches,on_delete=models.CASCADE)
    name= models.CharField(max_length=50,choices=test_name)
    status = models.BooleanField(default='False')

    class Meta:
        unique_together=(('teach','name'),)



    def total_marks(self):
        if self.name=='Insem':
            return 30
        return 20

