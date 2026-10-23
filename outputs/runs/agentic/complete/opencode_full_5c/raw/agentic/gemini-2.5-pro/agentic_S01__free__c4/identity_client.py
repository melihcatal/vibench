import firebase_admin
from firebase_admin import credentials
import os


def get_firebase_app():
    if not firebase_admin._apps:
        cred_path = os.environ.get("FIREBASE_ADMIN_SDK_CREDENTIALS")
        if cred_path:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            # For environments where GOOGLE_APPLICATION_CREDENTIALS is set
            firebase_admin.initialize_app()
    return firebase_admin.get_app()
