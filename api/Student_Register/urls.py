
from django.urls import include, path
from rest_framework import routers

from .views import VerifyVoterIdentity, VotersRegisterView, ValidateVoterId

router = routers.DefaultRouter()
router.register(r'student-register', VotersRegisterView, basename="voters")

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls)),
    path('verify/', VerifyVoterIdentity.as_view()),
    path('validate-voterid/', ValidateVoterId.as_view()),
    path('profiles/', include('Profiles.urls')),
    path('auth/',include('Authentication.urls')),
    # path('elections/',include('Elections.urls')),
    # path('candidates/',include('Candidates.urls')),
    # path('ballots/',include('Ballots.urls')),
    # path('votes/',include('Votes.urls')),
    # path('register/upload-register/<int:pk>', VoterRegisterUpload.as_view({'post': 'upload_list'})),
]
