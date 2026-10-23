import os
import firebase_admin
from firebase_admin import credentials, auth
from identity_client import get_firebase_app

def register_user(email, password):
    """
    Creates a new user account with email and password using Firebase Authentication.
    """
    app = get_firebase_app()
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {"uid": user.uid, "email": user.email, "message": "User registered successfully"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (requires Firebase project setup and credentials)
    # Ensure FIREBASE_CREDENTIALS_PATH environment variable is set
    # result = register_user("test@example.com", "securePassword123")
    # print(result)
    pass
