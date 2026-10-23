import os
from firebase_admin import auth, initialize_app
from firebase_admin.exceptions import FirebaseError
from identity_models import LoginRequest, LoginResponse
import requests

# Initialize Firebase Admin SDK
if not auth._apps:
    initialize_app(options={
        "projectId": os.getenv("FIREBASE_PROJECT_ID")
    })


def email_password_login(request: LoginRequest) -> LoginResponse:
    try:
        # Firebase REST API for email/password login
        rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={os.getenv('FIREBASE_API_KEY')}"
        payload = {
            "email": request.email,
            "password": request.password,
            "returnSecureToken": True
        }
        response = requests.post(rest_api_url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        return LoginResponse(
            success=True,
            id_token=data["idToken"],
            refresh_token=data["refreshToken"],
            expires_in=int(data["expiresIn"])
        )
    except (FirebaseError, requests.exceptions.RequestException) as e:
        return LoginResponse(
            success=False,
            error_message=str(e)
        )