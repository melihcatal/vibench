import os
import firebase_admin
from firebase_admin import credentials, auth

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_PATH"))
        firebase_admin.initialize_app(cred)

def register_user(email: str, password: str, display_name: str = None):
    initialize_firebase()
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        return {"uid": user.uid, "email": user.email, "message": "User registered successfully."}
    except Exception as e:
        return {"error": str(e)}

