from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from users.models import Student, Tutor

class RoleBasedAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            user_type = request.GET.get("type", None)
                
            if user_type == "staff" and Tutor.objects.filter(user=user).exists():
                return user  
            elif user_type != "staff" and Student.objects.filter(user=user).exists():
                return user 
            else:
                return None  
        except User.DoesNotExist:
            return None
