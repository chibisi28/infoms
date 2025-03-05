from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def add_course(request):
    return HttpResponse("Course added successfully")