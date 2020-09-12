from django.shortcuts import render,redirect,HttpResponseRedirect
from college_info.models import Assignment,Staff
from .forms import AssignmentForm
from .models import Teaches,PeriodTime
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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
        context['assignments']=Assignment.objects.filter(teach__batch__id=request.user.student.batch_id.id)
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