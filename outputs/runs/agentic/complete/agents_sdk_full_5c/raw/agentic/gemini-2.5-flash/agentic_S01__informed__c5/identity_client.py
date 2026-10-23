import firebase_admin
from firebase_admin import credentials, App
import os

def get_firebase_app() -> App:
    # Initialize Firebase Admin SDK if not already initialized
    # The GOOGLE_APPLICATION_CREDENTIALS environment variable should point to your service account key file.
    if not firebase_admin._apps:
        # You can specify a name if you need multiple Firebase apps in one project
        # For simplicity, we use the default app name here.
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, name='default')
    return firebase_admin.get_app('default')

if __name__ == '__main__':
    # Example of how to use it (for local testing, not part of the core functionality)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set
    # try:
    #     app = get_firebase_app()
    #     print("Firebase app initialized successfully.")
    #     print(f"App name: {app.name}")
    # except Exception as e:
    #     print(f"Error initializing Firebase app: {e}")
    pass
