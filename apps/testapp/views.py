from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsModeratorOrAdmin, IsAdminOnly, IsUserOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import status

class PublicDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Привет, {request.user.email}! Это обычные данные."})

class SecretModeratorView(APIView):
    permission_classes = [IsModeratorOrAdmin]

    def get(self, request):
        return Response({"message": f"Секретная панель! Твоя роль: {request.user.role}."})

class AdminPanelAPIView(APIView):
    permission_classes = [IsAdminOnly]

    def get(self, request):
        return Response({"message": "Добро пожаловать в панель администратора!"})

class UserDashboardAPIView(APIView):
    permission_classes = [IsUserOnly]

    def get(self, request):
        return Response({"message": "Личный кабинет пользователя"})

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view, permission_classes

# Это представление я сделал через функцию
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_stats(request):
    user = request.user
    data = {
        "email": user.email,
        "role": getattr(user, 'role', 'user'),
        "is_staff": user.is_staff,
        "date_joined": user.date_joined,
    }
    return Response(data)