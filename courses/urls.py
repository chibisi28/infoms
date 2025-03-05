from django.urls import path ,include , re_path
from . import views
 

urlpatterns = [
    path('add/', views.add_course),
]
 
