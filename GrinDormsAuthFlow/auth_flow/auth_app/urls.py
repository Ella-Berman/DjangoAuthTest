from django.urls import path, include

from . import views

urlpatterns = [
    
    path('', views.homepage, name=""),

    path('register', views.register, name="register"),

    path('my-login', views.my_login, name="my-login"),

    path('dashboard', views.dashboard, name="dashboard"),

    path('user-logout', views.user_logout, name="user-logout"),

    path("activate/<str:uidb64>/<str:token>/", views.activate, name="activate"),

   # path("password-reset", views.password_reset, name="password-reset"),

   # path("accounts/", include("django.contrib.auth.urls")),

]

