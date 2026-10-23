import os
import firebase_admin
from firebase_admin import credentials


def initialize_firebase():
    if not firebase_admin._apps:
        # GOOGLE_APPLICATION_CREDENTIALS environment variable is used automatically
        # by the firebase-admin library.
        firebase_admin.initialize_app()


def get_firebase_web_api_key():
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")
    return api_key
