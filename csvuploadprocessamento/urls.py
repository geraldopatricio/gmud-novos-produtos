from django.urls import path
from csvuploadprocessamento import views

urlpatterns = [
    path('', views.home, name='home'),
]