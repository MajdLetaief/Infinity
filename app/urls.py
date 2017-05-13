from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.LoginView, name='login'),
    url(r'^index/', views.AuthView, name='index'),
    url(r'^volume/', views.VolumeView, name='volume'),
    url(r'^addvolume/', views.AddVolumeView, name='addvolume'),
    url(r'^images/', views.ImageView, name='images'),
    url(r'^flavors/', views.FlavorsView, name='flavors'),
    url(r'^flavor/([0-9]+)/$', views.FlavorView, name='flavor'),
    url(r'^addflavor',views.AddFlavorView, name="addflavor"),
    ]