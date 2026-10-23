import os
from firebase_admin import auth, credentials

cred = credentials.Certificate("path/to/serviceAccountKey.json")
app = firebase_admin.initialize_app(cred)

def register_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return user.uid
    except Exception as e:
        raise e