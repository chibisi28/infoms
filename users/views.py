from django.contrib.auth import authenticate, login , logout
from django.shortcuts import render, redirect
from .models import Student , Tutor
from courses.models import Course
from enrollment.models import Enrollment
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required 

# Create your views here.    

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        user_type = request.GET.get("type", "student")  
        user = authenticate(request, username=username)
        if user:
            login(request, user)
            if user_type == "staff":
                if 'next' in request.POST: 
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('users:staff_dashboard')
            else:
                if 'next' in request.POST: 
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('users:student_dashboard')
        else:
              return render(request, "login.html",{ "error" :"Invalid credentials or role mismatch."})
    return render(request, "login.html")


def logout_view(request):
    if request.method == "POST":
        
        logout(request)
        return redirect("users:login")

@login_required(login_url="/users/login?type=student")
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('users:login')

    try:
        cours = Enrollment.objects.filter(student=student)
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found.")
        print("Student profile not found.")
    
    details = []
    
    for c in cours:
        details.append({"title": c.course.title, "code": c.course.code, "test": round(c.test), "exam": round(c.exam), "total": round(float(c.test) + float(c.exam))})
    
    context = {
        "gender": student.gender,
        "username": student.username,
        "profile_pic": student.profile_pic,
        "level": student.level,
        "Department": student.department,
        "registration_number": student.registration_number,
        "fullname": student.first_name + " " + student.last_name + " "  + student.other_name,
        "first_name": student.first_name ,
        "courses": details ,
    }
    return render(request, 'users/students/dashboard.html', context)


@login_required(login_url="/users/login?type=staff")
def staff_dashboard(request):
    try:
        tutor = Tutor.objects.get(user=request.user)
    except Tutor.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('users:login')

    try:
        cours = Course.objects.filter(tutor=tutor)
    except Tutor.DoesNotExist:
        messages.error(request, "Student profile not found.")
        print("Student profile not found.")
    
    details = []
    
    for c in cours:
        details.append({"id": c.id ,"title": c.title, "code": c.code, "level": c.level})

    context = {
        "gender": tutor.gender,
        "username": tutor.username,
        "courses_amount": len(details),
        "fullname": tutor.first_name + " " + tutor.last_name + " "  + tutor.other_name,
        "first_name": tutor.first_name ,
        "profile_pic": tutor.profile_pic ,
        "courses": details,
    }
    return render(request, 'users/lecturers/dashboard.html', context)