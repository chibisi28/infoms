from django.urls import path ,include , re_path
from . import views
 
app_name ='users'

urlpatterns = [
    path('login', views.login_view , name='login'),
    path('staff/dashboard', views.staff_dashboard , name='staff_dashboard'),
    path('student/dashboard', views.student_dashboard , name='student_dashboard'),
    path('log_out/', views.logout_view,name="log_out"), 
]
 
