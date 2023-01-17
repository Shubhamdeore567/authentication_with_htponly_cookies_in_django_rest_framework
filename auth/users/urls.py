from django.urls import path
from . import views

urlpatterns = [
    path("register/",views.Register.as_view()),
    path("login/",views.Login.as_view()),
    path("test/",views.GetUser.as_view()),
    path("logout/",views.LogOut.as_view()),
    path("verify_email/",views.VerifyEmail.as_view())
]