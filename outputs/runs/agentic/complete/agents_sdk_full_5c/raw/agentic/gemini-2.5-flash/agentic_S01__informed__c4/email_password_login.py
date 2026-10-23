import os
import firebase_admin
from firebase_admin import credentials, auth

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY_PATH"))
        firebase_admin.initialize_app(cred)

def email_password_login(id_token: str):
    """
    Verifies a Firebase ID token.
    Note: Actual email/password login and token acquisition usually happens client-side.
    This function demonstrates server-side verification of an ID token obtained client-side.
    """
    initialize_firebase()
    try:
        decoded_token = auth.verify_id_token(id_token)
        return {"uid": decoded_token["uid"], "email": decoded_token["email"], "message": "User ID token verified."}
    except Exception as e:
        return {"error": str(e)}

