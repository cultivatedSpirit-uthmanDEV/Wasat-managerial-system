from . import views
from django.urls import path


urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.login, name='logout'),
    path("", views.welcome, name="welcome"),
]

