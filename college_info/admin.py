from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from college_info.models import User,Course,Batch,Teaches,Student,Dept,Staff,Assignment

class BatchInline(admin.TabularInline):
    model= Batch
    extra=0

class StudentInline(admin.TabularInline):
    model = Student
    extra=0

class DeptAdmin(admin.ModelAdmin):
    inlines = [BatchInline]
    list_display = ('name','id')

class BatchAdmin(admin.ModelAdmin):
    inlines = [StudentInline]
    list_display = ('id','department','section','sem')

class CourseAdmin(admin.ModelAdmin):
    list_display =('id','name','department')

class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no','name','batch_id')
    ordering = ('batch_id__department__name','batch_id__id','roll_no')

class StaffAdmin(admin.ModelAdmin):
    list_display =('id','name','department')

class TeachesAdmin(admin.ModelAdmin):
    list_display = ('batch','course','staff')
    ordering = ('batch__department__name','batch__id','course__id')

class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('teach','submission_date')

admin.site.register(User,UserAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Batch,BatchAdmin)
admin.site.register(Teaches,TeachesAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Dept,DeptAdmin)
admin.site.register(Staff,StaffAdmin)
admin.site.register(Assignment,AssignmentAdmin)