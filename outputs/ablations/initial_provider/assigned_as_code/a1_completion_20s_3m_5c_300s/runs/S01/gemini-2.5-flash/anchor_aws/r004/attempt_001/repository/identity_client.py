import firebase_admin
from firebase_admin import credentials, auth
import os

def get_firebase_client():
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.environ.get("FIREBASE_ADMIN_SDK_PATH"))
        firebase_admin.initialize_app(cred)
    return auth
