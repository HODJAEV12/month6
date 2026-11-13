import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


def get_google_access_token(code: str) -> str:
    url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    
    response = requests.post(url, data=payload)
    data = response.json()
    
    if "error" in data:
        raise AuthenticationFailed("Не удалось получить токен от Google")
        
    return data.get("access_token")


def get_google_user_info(access_token: str) -> dict:
    url = "https://www.googleapis.com/oauth2/v3/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    if "error" in data or "email" not in data:
        raise AuthenticationFailed("Не удалось получить данные профиля от Google")
        
    return data