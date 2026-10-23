import os
import firebase_admin
from firebase_admin import credentials, auth

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_PATH"))
        firebase_admin.initialize_app(cred)

def password_reset(email: str):
    initialize_firebase()
    try:
        link = auth.generate_password_reset_link(email)
        return {"email": email, "password_reset_link": link, "message": "Password reset link generated."}
    except Exception as e:
        return {"error": str(e)}

