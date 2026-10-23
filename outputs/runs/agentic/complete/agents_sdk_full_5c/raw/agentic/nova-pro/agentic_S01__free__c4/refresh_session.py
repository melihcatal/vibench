import firebase_admin
from firebase_admin import auth

def refresh_session(refresh_token):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    new_tokens = auth.refresh_id_token(refresh_token)
    return new_tokens