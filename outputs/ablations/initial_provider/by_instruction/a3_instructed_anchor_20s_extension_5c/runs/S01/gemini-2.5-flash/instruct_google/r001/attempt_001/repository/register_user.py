from firebase_admin import auth
from identity_client import initialize_firebase_admin
from identity_models import create_user_response

initialize_firebase_admin()

def register_user(email, password):
    """
    Registers a new user with email and password using Google Firebase Authentication.
    """
    try:
        user = auth.create_user(email=email, password=password)
        return create_user_response(user.uid, user.email, "User registered successfully")
    except Exception as e:
        return {"error": str(e)}
