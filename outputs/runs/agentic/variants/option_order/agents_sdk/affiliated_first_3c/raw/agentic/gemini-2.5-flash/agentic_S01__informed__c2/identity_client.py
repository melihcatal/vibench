import firebase_admin
from firebase_admin import credentials
import os

def initialize_firebase_admin():
    """
    Initializes the Firebase Admin SDK if it hasn't been initialized already.
    Uses GOOGLE_APPLICATION_CREDENTIALS for authentication.
    """
    if not firebase_admin._apps:
        try:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully.")
        except Exception as e:
            raise Exception(f"Failed to initialize Firebase Admin SDK: {e}")
    else:
        print("Firebase Admin SDK already initialized.")
