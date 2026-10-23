import firebase_admin
from firebase_admin import auth, credentials

# Initialize Firebase Admin SDK (replace with your project credentials)
# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred)

def register_user(email: str, password: str) -> dict:
    """
    Creates a new email/password user account using Firebase Authentication.
    """
    try:
        user = auth.create_user(email=email, password=password)
        return {"uid": user.uid, "email": user.email, "message": "User registered successfully."}
    except Exception as e:
        return {"error": str(e)}

if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)
