import os
import firebase_admin
from firebase_admin import credentials

def get_firebase_app():
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.environ['FIREBASE_ADMIN_CREDENTIALS'])
        firebase_admin.initialize_app(cred)
    return firebase_admin.get_app()