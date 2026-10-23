import os
from firebase_admin import credentials, initialize_app

# Initialize the Firebase Admin SDK
cred = credentials.Certificate("path/to/serviceAccountKey.json")
app = initialize_app(cred)


def get_firebase_client():
    return app
