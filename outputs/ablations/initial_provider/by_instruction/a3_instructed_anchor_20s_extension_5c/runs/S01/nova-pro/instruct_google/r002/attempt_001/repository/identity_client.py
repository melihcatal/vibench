import firebase_admin
from firebase_admin import credentials

def initialize_firebase_app():
    cred = credentials.Certificate('path/to/serviceAccountKey.json')
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)