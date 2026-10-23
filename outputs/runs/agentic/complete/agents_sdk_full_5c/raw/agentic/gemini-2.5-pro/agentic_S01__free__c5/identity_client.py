import os
import pyrebase

def get_auth_client():
    """
    Initializes and returns the Pyrebase authentication client.
    Configuration is loaded from environment variables.
    """
    firebase_config = {
        "apiKey": os.environ.get("FIREBASE_API_KEY"),
        "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN"),
        "databaseURL": os.environ.get("FIREBASE_DATABASE_URL"),
        "projectId": os.environ.get("FIREBASE_PROJECT_ID"),
        "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.environ.get("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.environ.get("FIREBASE_APP_ID"),
    }
    
    if not all(firebase_config.values()):
        raise ValueError("One or more Firebase environment variables are not set.")

    firebase = pyrebase.initialize_app(firebase_config)
    return firebase.auth()
