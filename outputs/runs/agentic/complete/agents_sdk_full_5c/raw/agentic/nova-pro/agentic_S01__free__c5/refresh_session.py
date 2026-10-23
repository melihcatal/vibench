import firebase_admin
from firebase_admin import auth

def refresh_session(id_token):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    verified_id_token = auth.verify_id_token(id_token)
    new_token = auth.create_custom_token(verified_id_token['uid'])
    return new_token