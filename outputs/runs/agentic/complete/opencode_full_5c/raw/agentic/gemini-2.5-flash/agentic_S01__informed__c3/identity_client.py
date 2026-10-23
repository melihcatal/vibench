import firebase_admin
from firebase_admin import credentials, auth
import os


def get_firebase_app():
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
        firebase_admin.initialize_app(cred)
    return firebase_admin.get_app()


def get_auth_client():
    return auth
