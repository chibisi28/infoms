
from django.contrib import admin
from django.urls import path ,include , re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
# from django.views.static import serve
from django.conf.urls import handler404
from django.shortcuts import render

# Custom 404 view
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

# Set Django to use the custom handler
handler404 = custom_404_view


urlpatterns = [
    # re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('', views.landing),
    
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')), 
    path('enrollment/', include('enrollment.urls')),
]

urlpatterns += static(settings.MEDIA_URL , document_root= settings.MEDIA_ROOT) 
