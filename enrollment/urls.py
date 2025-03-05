from django.urls import path 
from . import views
 
app_name = 'enrollment'

urlpatterns = [
    path('edit_grade/<int:id>', views.edit_grade, name='edit_grade'),
    path('save_grade/<int:id>', views.save_grade, name='save_grade'),
    path('grade/<int:id>', views.grade, name='grade'),
]
 
