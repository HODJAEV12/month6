from django.urls import path
from apps.testapp.views import (
    AdminPanelAPIView, CustomTokenObtainPairView, 
    GoogleAuthView, LogoutView, PublicDataView, 
    SecretModeratorView, UserDashboardAPIView, profile_stats
)

urlpatterns = [
    path('public/', PublicDataView.as_view(), name='public-data'),
    path('secret/', SecretModeratorView.as_view(), name='secret-data'),
    path('admin-panel/', AdminPanelAPIView.as_view(), name='admin-panel'),
    path('user-dashboard/', UserDashboardAPIView.as_view(), name='user-dashboard'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/stats/', profile_stats, name='profile_stats'),
    path("auth/google/", GoogleAuthView.as_view(), name="google-auth"),
]