import os
import requests
from identity_models import EmailPasswordLoginRequest, EmailPasswordLoginResponse

FIREBASE_WEB_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
if not FIREBASE_WEB_API_KEY:
    raise EnvironmentError("FIREBASE_WEB_API_KEY environment variable not set.")

FIREBASE_SIGN_IN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"

def email_password_login(request: EmailPasswordLoginRequest) -> EmailPasswordLoginResponse:
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True
    }
    response = requests.post(FIREBASE_SIGN_IN_URL, json=payload)
    response.raise_for_status()
    data = response.json()
    
    return EmailPasswordLoginResponse(
        id_token=data["idToken"],
        refresh_token=data["refreshToken"],
        expires_in=int(data["expiresIn"]),
        local_id=data["localId"]
    )