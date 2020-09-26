"""College_Management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from college_info import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',LoginView.as_view(template_name= 'college_info/login.html'),name='login'),
    path('logout/',LogoutView.as_view(template_name='college_info/logout.html'),name='logout'),
    path('home/',views.home,name='home'),
    path('student/timetable/<slug:batch_id>/',views.student_timetable,name='student_timetable'),
    path('student/attendance/<slug:stud_roll_no>/',views.student_attendance,name='student_attendance'),
    path('student/marks/<slug:stud_roll_no>/',views.student_marks,name='student_marks'),
    path('staff/timetable/<slug:staff_id>/',views.staff_timetable,name='staff_timetable'),
    path('staff/teaches/<slug:staff_id>/<int:choice>/',views.staff_teaches,name='staff_teaches'),
    path('staff/ClassDates/<slug:teaches_id>/<slug:course_id>/',views.class_dates,name='staff_class_dates'),
    path('staff/Attendance/<int:batch_attendance_id>/',views.staff_attendance,name='staff_attendance'),
    path('staff/Attendance/<int:batch_attendance_id>/confirm',views.staff_attendance_confirm,name='staff_attendance_confirm'),
    path('staff/CancelClass/<int:batch_attendance_id>/',views.cancel_class,name='cancel_class'),
    path('staff/EditAttendance/<int:batch_attendance_id>/',views.edit_attendance,name='edit_attd'),
    path('staff/MarksList/<slug:teaches_id>/',views.staff_marks_list,name='marks_list'),
    path('staff/EnterMarks/<slug:markclass_id>/',views.staff_enter_marks,name='enter_marks'),
    path('staff/EnterMarks/<slug:markclass_id>/confirm',views.staff_marks_confirm,name='marks_confirm'),
    path('staff/EditMarks/<slug:markclass_id>/',views.staff_edit_marks,name='edit_marks'),
    path('staff/student/marks/<slug:teaches_id>/',views.staff_student_marks,name='staff_student_marks'),
    path('staff/check_submissions/<slug:assignment_id>',views.check_submission,name='check_submission'),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
