from django.db import models
from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser

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
