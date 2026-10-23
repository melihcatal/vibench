import os
from firebase_admin import auth

def initialize_firebase_app():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/serviceAccountKey.json'

def create_user(email, password):
    user = auth.create_user(email=email, password=password)
    return user.uid

def get_user(uid):
    user = auth.get_user(uid)
    return user.email

def delete_user(uid):
    auth.delete_user(uid)