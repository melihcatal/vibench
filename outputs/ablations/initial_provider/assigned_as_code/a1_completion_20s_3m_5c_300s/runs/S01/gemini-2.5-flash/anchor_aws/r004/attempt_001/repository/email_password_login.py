from identity_client import get_firebase_client
from identity_models import UserLoginRequest, UserLoginResponse
import requests
import os

def email_password_login(request: UserLoginRequest):
    api_key = os.environ.get("FIREBASE_API_KEY")
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True
    }
    response = requests.post(rest_api_url, json=payload).json()
    if "error" in response:
        raise Exception(response["error"]["message"])
    return UserLoginResponse(
        id_token=response["idToken"],
        refresh_token=response["refreshToken"],
        uid=response["localId"]
    )
