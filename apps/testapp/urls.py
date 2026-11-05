from django.urls import path
from apps.testapp.views import (
    AdminPanelAPIView, PublicDataView, 
    SecretModeratorView, UserDashboardAPIView
)

urlpatterns = [
    path('public/', PublicDataView.as_view(), name='public-data'),
    path('secret/', SecretModeratorView.as_view(), name='secret-data'),
    path('admin-panel/', AdminPanelAPIView.as_view(), name='admin-panel'),
    path('user-dashboard/', UserDashboardAPIView.as_view(), name='user-dashboard'),
]