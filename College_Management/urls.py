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
    path('staff/timetable/<slug:staff_id>/',views.staff_timetable,name='staff_timetable'),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
