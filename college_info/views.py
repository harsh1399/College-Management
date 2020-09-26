from django.shortcuts import render,redirect,HttpResponseRedirect
from college_info.models import Assignment,Staff
from .forms import AssignmentForm,AttendanceForm
from .models import Teaches,PeriodTime,BatchAttendance,Attendance,Student,AttendanceTotal,MarksClass,StudentCourse,Course,Submission
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required()
def home(request):
    context={}
    if request.user.is_teacher:
        if request.method == 'POST':
            form = AssignmentForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = AssignmentForm()
            form.fields['teach'].queryset=Teaches.objects.filter(staff__id=request.user.staff.id)
            context['assignments']=Assignment.objects.filter(teach__staff__id=request.user.staff.id)
            context['form']=form
        return render(request,'college_info/staff_home.html',context)
    else:
        if request.method=='POST':
            assignment = request.POST['assignment']
            submit = request.FILES['submitfile']
            student = request.user.student
            assign = Assignment.objects.get(id=assignment)
            submission = Submission(assignment=assign,student=student,doc=submit)
            submission.save()
            return redirect('home')
        else:
            #form = SubmissionForm()
            context['assignments']=Assignment.objects.filter(teach__batch__id=request.user.student.batch_id.id)
            #context['form']=form
            sub_objs= Submission.objects.filter(student=request.user.student)
            l=[]
            for obj in sub_objs:
                a = Assignment.objects.get(submission=obj)
                l.append(a)
            context['submitted']=l
            context['submissions']=sub_objs
    return render(request,'college_info/home.html',context)

@login_required()
def student_timetable(request,batch_id):
    period_time = PeriodTime.objects.filter(teach__batch__id = batch_id)
    timetable = [['' for i in range(8)] for j in range(5)]
    for index,day in enumerate(PeriodTime.DayOfWeek):
        time_slot = 0
        for slot in range(8):
            if slot == 0:
                timetable[index][0]=day[0]
                continue
            elif slot == 3 or slot == 6:
                continue
            try:
                a = period_time.get(period=PeriodTime.TimeSlots[time_slot][0],day=day[0])
                timetable[index][slot]=a.teach.course.id+"\n("+a.teach.staff.name+")"
            except PeriodTime.DoesNotExist:
                pass
            time_slot += 1

    context = {'timetable':timetable}
    return render(request,'college_info/student_timetable.html',context)

@login_required()
def staff_timetable(request,staff_id):
    period_time = PeriodTime.objects.filter(teach__staff__id=staff_id)
    timetable = [['' for i in range(8)] for j in range(5)]
    for index, day in enumerate(PeriodTime.DayOfWeek):
        time_slot = 0
        for slot in range(8):
            if slot == 0:
                timetable[index][0] = day[0]
                continue
            elif slot == 3 or slot == 6:
                continue
            try:
                a = period_time.get(period=PeriodTime.TimeSlots[time_slot][0], day=day[0])
                timetable[index][slot] = a.teach.course.id + "\n(" + a.teach.staff.name + ")"
            except PeriodTime.DoesNotExist:
                pass
            time_slot += 1

    context = {'timetable': timetable}
    return render(request, 'college_info/staff_timetable.html', context)

@login_required()
def staff_teaches(request,staff_id,choice):
    staff = Staff.objects.get(id=staff_id)
    context={
        'staff':staff,
        'choice':choice
    }
    return render(request,'college_info/staff_teaches.html',context)

@login_required()
def class_dates(request,teaches_id,course_id):
    if request.method == 'POST':
        form =AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('staff_class_dates',args=(teaches_id,course_id)))
    else:
        now = timezone.now()
        form = AttendanceForm()
        #form.fields['teach'].queryset = Teaches.objects.filter(staff__id=request.user.staff.id)
        form.fields['teach'].queryset = Teaches.objects.filter(course__id = course_id)
        teach = Teaches.objects.get(id = teaches_id)
        batch_attendance = teach.batchattendance_set.filter(date__lte=now).order_by('-date')
    return render(request,'college_info/class_dates.html',{'batch_attendance':batch_attendance,'form':form})

@login_required()
def staff_attendance(request,batch_attendance_id):
    batch_attendance=BatchAttendance.objects.get(id=batch_attendance_id)
    teach =batch_attendance.teach
    batch =teach.batch
    context ={
        'batch_attendance':batch_attendance,
        'teach':teach,
        'batch':batch
    }
    return render(request,'college_info/staff_attendance.html',context)

@login_required()
def staff_attendance_confirm(request,batch_attendance_id):
    btch_attd = BatchAttendance.objects.get(id=batch_attendance_id)
    tch=btch_attd.teach
    crs = tch.course
    btch = tch.batch
    for index,student in enumerate(btch.student_set.all()):
        status = request.POST[student.roll_no]
        if status == 'present':
            status = 'True'
        else:
            status='False'
        if btch_attd.status == 1:
            try:
                a= Attendance.objects.get(course=crs,student=student,date=btch_attd.date,batch_attendance=btch_attd)
                a.status=status
                a.save()
            except Attendance.DoesNotExist:
                a = Attendance(course=crs, student=student,status=status, date=btch_attd.date,batch_attendance=btch_attd)
                a.save()
        else:
            a = Attendance(course=crs, student=student, status=status, date=btch_attd.date,batch_attendance=btch_attd)
            a.save()
            btch_attd.status=1
            btch_attd.save()
    return HttpResponseRedirect(reverse('staff_class_dates',args=(tch.id,crs.id)))

login_required()
def cancel_class(request,batch_attendance_id):
    batch_attendance = BatchAttendance.objects.get(id=batch_attendance_id)
    batch_attendance.status=2
    batch_attendance.save()
    return HttpResponseRedirect(reverse('staff_class_dates', args=(batch_attendance.teach.id,batch_attendance.teach.course.id)))

@login_required()
def edit_attendance(request,batch_attendance_id):
    batch_attendance= BatchAttendance.objects.get(id=batch_attendance_id)
    course = batch_attendance.teach.course
    att_list = Attendance.objects.filter(batch_attendance=batch_attendance,course=course)
    return render(request,'college_info/staff_edit_attendance.html',{'att_list':att_list,'batch_attendance':batch_attendance})

@login_required()
def student_attendance(request,stud_roll_no):
    student = Student.objects.get(roll_no=stud_roll_no)
    teaches = Teaches.objects.filter(batch__id=student.batch_id.id)
    attended_list=[]
    for teach in teaches:
        try:
            a =AttendanceTotal.objects.get(student = student,course=teach.course)
        except AttendanceTotal.DoesNotExist:
            a= AttendanceTotal(student=student,course=teach.course)
            a.save()
        attended_list.append(a)
    return render(request,'college_info/student_attendance.html',{'att_list':attended_list})

@login_required()
def staff_marks_list(request,teaches_id):
    teach = Teaches.objects.get(id=teaches_id)
    mark_class_list=MarksClass.objects.filter(teach=teach)
    return render(request,'college_info/staff_marks_list.html',{'mlist':mark_class_list})

@login_required()
def staff_enter_marks(request,markclass_id):
    markclass=MarksClass.objects.get(id=markclass_id)
    teach = markclass.teach
    batch=teach.batch
    context={
        'teach':teach,
        'batch':batch,
        'markclass':markclass
    }
    return render(request,'college_info/staff_enter_marks.html',context)

@login_required()
def staff_marks_confirm(request,markclass_id):
    markclass = MarksClass.objects.get(id=markclass_id)
    teach = markclass.teach
    course = teach.course
    batch =teach.batch
    for student in batch.student_set.all():
        mark = request.POST[student.roll_no]
        sc = StudentCourse.objects.get(student=student,course=course)
        m = sc.marks_set.get(name=markclass.name)
        m.marks=mark
        m.save()
    markclass.status = True
    markclass.save()
    return HttpResponseRedirect(reverse('marks_list',args=(teach.id,)))

@login_required()
def staff_edit_marks(request,markclass_id):
    markclass = MarksClass.objects.get(id=markclass_id)
    course = markclass.teach.course
    student_list = markclass.teach.batch.student_set.all()
    marks_list=[]
    for student in student_list:
        sc = StudentCourse.objects.get(student=student,course=course)
        marks = sc.marks_set.get(name = markclass.name)
        marks_list.append(marks)
    return render(request,'college_info/staff_edit_marks.html',{'markclass':markclass,'markslist':marks_list})

@login_required()
def staff_student_marks(request,teaches_id):
    teach = Teaches.objects.get(id=teaches_id)
    sclist = StudentCourse.objects.filter(student__in=teach.batch.student_set.all(),course=teach.course)
    return render(request,'college_info/staff_student_marks.html',{'sclist':sclist})

@login_required()
def student_marks(request,stud_roll_no):
    student= Student.objects.get(roll_no=stud_roll_no)
    teach_list = Teaches.objects.filter(batch__id = student.batch_id.id)
    sclist=[]
    for teach in teach_list:
        sc= StudentCourse.objects.get(student=student,course=teach.course)
        sclist.append(sc)
    return render(request,'college_info/student_marks_list.html',{'sclist':sclist})

@login_required()
def check_submission(request,assignment_id):
    submissions= Submission.objects.filter(assignment__id= assignment_id)
    assignment = Assignment.objects.get(id = assignment_id)
    context={
        'submissions':submissions,
        'assignment':assignment
    }
    return render(request,'college_info/staff_check_submission.html',context)