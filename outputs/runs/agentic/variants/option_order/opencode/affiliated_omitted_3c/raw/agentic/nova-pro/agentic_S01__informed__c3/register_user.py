import os
from firebase_admin import auth

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"


def register_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return user.uid
    except Exception as e:
        return str(e)
