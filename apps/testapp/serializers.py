from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        data.update({
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
            'role': getattr(self.user, 'role', 'user'), 
        })
        return data

class GoogleAuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)