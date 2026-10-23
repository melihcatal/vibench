import firebase_admin
from firebase_admin import credentials, auth

def refresh_session(refresh_token):
    if not firebase_admin._apps:
        cred = credentials.Certificate('path/to/serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
    new_token = auth.refresh_id_token(refresh_token)
    return new_token