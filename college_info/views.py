from django.shortcuts import render

def home(request):
    if request.user.is_teacher:
        return render(request,'college_info/staff_home.html')
    else:
        return render(request,'college_info/home.html')

