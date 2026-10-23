import firebase_admin
from firebase_admin import auth

firebase_admin.initialize_app()

def refresh_session(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        new_token = auth.create_custom_token(uid)
        return new_token
    except firebase_admin.auth.TokenExpiredError:
        return 'Token expired'