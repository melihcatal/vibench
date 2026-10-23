import os
from firebase_admin import auth, credentials

cred = credentials.Certificate("path/to/serviceAccountKey.json")
app = firebase_admin.initialize_app(cred)

def get_client():
    return auth