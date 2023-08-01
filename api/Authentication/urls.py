from .views import *
from rest_framework import routers
from django.urls import path, include 
from knox import views as knox_views 


urlpatterns = [
	path('register', SignUpAPI.as_view()),
	path('login', SignInAPI.as_view()),
	path('check_username',UsernameAPI.as_view()),
	path('send_otp',SendOTPViewSet.as_view()),
	path('verify_otp',VerifyOTPViewSet.as_view()),
	path('logout', knox_views.LogoutView.as_view(), name="knox-logout"),

] 