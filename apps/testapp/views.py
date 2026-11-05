from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsModeratorOrAdmin, IsAdminOnly, IsUserOnly

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
        # Проверка роли пользователя перед возвратом данных(дополнение от себя)
        if request.user.role != 'user':
            return Response({"message": "Доступ запрещен. Только пользователи могут видеть это."})

        return Response({"message": "Личный кабинет пользователя"})