import os
import firebase_admin
from firebase_admin import credentials, auth
from identity_client import get_firebase_app
from identity_models import RegisterUserRequest, RegisterUserResponse

def register_new_user(request: RegisterUserRequest) -> RegisterUserResponse:
    app = get_firebase_app()
    try:
        user = auth.create_user(email=request.email, password=request.password)
        return RegisterUserResponse(uid=user.uid, email=user.email, email_verified=user.email_verified)
    except Exception as e:
        raise ValueError(f"Firebase user registration failed: {e}")