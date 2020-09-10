from django.shortcuts import render,redirect,HttpResponseRedirect
from college_info.models import Assignment
from .forms import AssignmentForm
from .models import Teaches
from django.urls import reverse
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

