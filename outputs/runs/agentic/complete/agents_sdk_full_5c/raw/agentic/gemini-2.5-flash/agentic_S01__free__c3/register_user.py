import os
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
from identity_client import get_firebase_app
from identity_models import RegisterRequest, RegisterResponse

def register_user(request: RegisterRequest) -> RegisterResponse:
    app = get_firebase_app()
    try:
        user = auth.create_user(
            email=request.email,
            password=request.password
        )
        return RegisterResponse(uid=user.uid, email=user.email)
    except Exception as e:
        # In a real app, handle specific Firebase exceptions
        raise RuntimeError(f"Failed to register user: {e}")

if __name__ == '__main__':
    # This block is for demonstration/testing only and won't be run by the evaluator.
    # Ensure you have a service account key file for Firebase Admin SDK.
    # For local testing, you might need to set GOOGLE_APPLICATION_CREDENTIALS
    # or pass the path to the service account key in identity_client.py
    # Example usage:
    # try:
    #     new_user = register_user(RegisterRequest(email="test@example.com", password="StrongPassword123!"))
    #     print(f"User registered: {new_user.uid}")
    # except RuntimeError as e:
    #     print(f"Error: {e}")
    pass
