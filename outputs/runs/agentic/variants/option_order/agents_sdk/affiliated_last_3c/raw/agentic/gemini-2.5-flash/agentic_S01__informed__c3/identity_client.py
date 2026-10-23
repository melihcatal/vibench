import firebase_admin
from firebase_admin import credentials
import os

def initialize_firebase_app():
    """
    Initializes the Firebase Admin SDK.
    Looks for GOOGLE_APPLICATION_CREDENTIALS environment variable.
    """
    if not firebase_admin._apps:
        try:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully.")
        except Exception as e:
            print(f"Error initializing Firebase Admin SDK: {e}")
            print("Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.")
    else:
        print("Firebase Admin SDK already initialized.")

# Example of how you might use it (e.g., in a main application entry point)
if __name__ == '__main__':
    initialize_firebase_app()
    # You can then use firebase_admin.auth etc. in other modules
