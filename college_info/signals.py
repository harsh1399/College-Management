from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Teaches,MarksClass,Marks,StudentCourse,test_name,Student

@receiver(post_save,sender=Teaches)
def create_mark_class(sender,instance,created,**kwargs):
    if created:
        for name in test_name:
            try:
                MarksClass.objects.get(teach=instance,name=name[0])
            except MarksClass.DoesNotExist:
                a = MarksClass(teach=instance,name=name[0])
                a.save()


@receiver(post_save,sender=Student)
@receiver(post_save,sender=Teaches)
def create_marks(sender,instance,created,**kwargs):
    if created:
        if hasattr(instance,'name'):
            teach_list = instance.batch_id.teaches_set.all()
            for teach in teach_list:
                try:
                    StudentCourse.objects.get(student=instance,course=teach.course)
                except StudentCourse.DoesNotExist:
                    sc = StudentCourse(student=instance,course=teach.course)
                    sc.save()
                    sc.marks_set.create(name='Insem')
                    sc.marks_set.create(name='Term Work')

        elif hasattr(instance,'course'):
            student_list=instance.batch.student_set.all()
            course= instance.course
            for student in student_list:
                try:
                    StudentCourse.objects.get(student=student,course=course)
                except StudentCourse.DoesNotExist:
                    sc = StudentCourse(student=student,course=course)
                    sc.save()
                    sc.marks_set.create(name='Insem')
                    sc.marks_set.create(name='Term Work')
