from django.urls import path, include
from rest_framework import routers
from .views import ProfileViewSet
 #, UpdateProfileDetail

router = routers.DefaultRouter()

router.register('', ProfileViewSet)

urlpatterns = [
    path('', include(router.urls))
    # path('detail/<int:pk>', ProfileDetail.as_view(), name='view_profile_detail'),
    # path('update/<int:pk>', UpdateProfileDetail.as_view(), name='update profiles'),
   
   
]