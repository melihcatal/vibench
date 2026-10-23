import firebase_admin
from firebase_admin import auth

def refresh_session(refresh_token):
    if not firebase_admin._apps:
        firebase_admin.initialize_app()
    try:
        decoded_token = auth.verify_id_token(refresh_token)
        uid = decoded_token['uid']
        new_token = auth.create_custom_token(uid)
        return new_token
    except firebase_admin.auth.AuthError as e:
        raise Exception('Invalid refresh token') from e