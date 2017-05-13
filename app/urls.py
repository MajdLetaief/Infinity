from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.LoginView, name='login'),
    url(r'^index/', views.AuthView, name='index'),
    ]