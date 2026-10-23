import firebase_admin
from firebase_admin import credentials, auth
import os

FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID")

def initialize_firebase_app():
    if not firebase_admin._apps:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {"projectId": FIREBASE_PROJECT_ID})
    return firebase_admin.get_app()

def get_firebase_auth_client():
    app = initialize_firebase_app()
    return auth



