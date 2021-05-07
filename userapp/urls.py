
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name="index"),
    path('signup', views.signup, name="singup"),
    path('home', views.home, name="home"),
    path('results', views.results, name="results"),
    path('createnewuser', views.createnewuser, name="createnewuser"),
    path('logout', views.logout, name="logout"),
    path('test', views.test, name="test"),
    path('continueasguest', views.continueasguest, name="continueasguest"),
]
