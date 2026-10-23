import os
import firebase_admin
from firebase_admin import auth

cred = firebase_admin.credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

def register_user(email, password):
    user = auth.create_user(email=email, password=password)
    return user.uid