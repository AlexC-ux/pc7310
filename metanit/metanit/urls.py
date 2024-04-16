from startapp import views
from django.contrib import admin
from django.urls import re_path, path

urlpatterns = [
    re_path('^.{0,1}$', views.index, name='home'),
    re_path(r'^about.$', views.about, name='about'),
    re_path(r'^contact.$', views.contact, name='contact'),
    path('admin/', admin.site.urls),
]

admin.site.site_title = "Админка"
admin.site.site_header = "Админка"
admin.site.index_title = "Панель администрирования"