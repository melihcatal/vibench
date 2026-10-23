import os
import firebase_admin
from firebase_admin import credentials, auth

def initialize_firebase_app():
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    firebase_admin.initialize_app(cred)

def get_auth_client():
    return auth