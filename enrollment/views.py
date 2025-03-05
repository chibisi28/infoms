from django.shortcuts import render , redirect ,get_object_or_404

from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import HttpResponse
from courses.models import Course
from enrollment.models import Enrollment
from django.contrib.auth.decorators import login_required 
# Create your views here.

@login_required(login_url="/users/login?type=staff")
def grade(request,id):
    course = Course.objects.get(id=id)
    enrollments = Enrollment.objects.filter(course=course)
    code = course.code
    
    student_list = []
    for student in enrollments:
        student_list.append({"id":student.id,"name": f"{student.student.user.first_name } {student.student.user.last_name} {student.student.other_name}","reg_no": f"{student.student.registration_number}","test": student.test,"exam": student.exam, "total" : round(float(student.test) + float(student.exam))})
        
        
    return render(request, "enrollment/grade.html" , {"student_list" : student_list , "code": code })

@login_required(login_url="/users/login?type=staff")
def edit_grade(request,id):
    enrollments = Enrollment.objects.get(id=id)
    course = enrollments.course
    code = course.code + " - " + enrollments.student.registration_number
    
    context = {"id": id ,"name": f"{enrollments.student.first_name } {enrollments.student.last_name} {enrollments.student.other_name}","reg_no": f"{enrollments.student.registration_number}","test": enrollments.test,"exam": enrollments.exam, "total" : round(float(enrollments.test) + float(enrollments.exam))}
    return render(request, "enrollment/edit_grade.html",{"context": context, "code": code})

@login_required(login_url="/users/login?type=staff")
def save_grade(request,id):

    if request.method == "POST":
        if not request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to edit scores.")
       
        enrollments = get_object_or_404(Enrollment, id=id)
        course = enrollments.course.id
        test_score = request.POST.get("test")
        exam_score = request.POST.get("exam")
        if request.user.username != enrollments.course.tutor.username:
            messages.error(request,"You are not allowed to edit this student's scores.")
        if not (0 <= float(test_score) <= 30): 
            messages.error(request, "Test score is out of range.")
            return redirect(f"/enrollment/edit_grade/{id}")  
        if not (0 <= float(exam_score) <= 70):
            messages.error(request, "Exam score is out of range.")
            return redirect(f"/enrollment/edit_grade/{id}")  
        else:
            try:
                enrollments.test = float(test_score)
                enrollments.exam = float(exam_score)
                enrollments.save()
                messages.success(request, "Grade updated successfully!")
            except ValueError:
                messages.error(request, "Invalid input! Please enter valid numbers.")
            return redirect(f"/enrollment/grade/{course}")  
    return render(request, "enrollment/edit_grade.html")