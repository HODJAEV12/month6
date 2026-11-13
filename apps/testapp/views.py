import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsModeratorOrAdmin, IsAdminOnly, IsUserOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import status
from .serializers import GoogleAuthSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .services import get_google_access_token, get_google_user_info


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


# ---------- OAuth2.0 ----------

User = get_user_model()

class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        code = serializer.validated_data["code"]
        
        access_token = get_google_access_token(code)
        user_info = get_google_user_info(access_token)
        
        email = user_info.get("email")
        name = user_info.get("name", "")
        
        user, created = User.objects.filter(email=email).first(), False
        if not user:
            username = f"{email.split('@')[0]}_{uuid.uuid4().hex[:6]}"
            user = User.objects.create(
                email=email,
                username=username,
                first_name=name
            )
            user.set_unusable_password()
            user.save()
            created = True
        
        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email
        refresh["role"] = getattr(user, "role", "client")
        
        return Response({
            "is_new_user": created,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
            },
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)