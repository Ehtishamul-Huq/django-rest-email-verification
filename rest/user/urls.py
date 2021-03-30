from django.conf.urls import url
from user.views import UserRegistrationView, UserLoginView, VerifyEmail, ForgotPassView, ChangePassView
from django.urls import path

urlpatterns = [
    url(r'^signup', UserRegistrationView.as_view()),
    url(r'^signin', UserLoginView.as_view()),  
    path('email-verify/<str:pk>/', VerifyEmail.as_view()),  
    path('forgot-pass/', ForgotPassView.as_view()),  
    path('change-pass/<str:pk>/', ChangePassView.as_view()),
    ]