from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.LoginView, name='login'),
    url(r'^index/', views.AuthView, name='index'),
    url(r'^volume/', views.VolumeView, name='volume'),
    url(r'^network/', views.GetNetwork, name='networks'),
    url(r'^addvolume/', views.AddVolumeView, name='addvolume'),
    url(r'^addnetwork/', views.AddNetworkView, name='addnetwork'),
    url(r'^images/', views.ImageView, name='images'),
    url(r'^fip/', views.FipView, name='fip'),

    ]