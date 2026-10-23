import os
from firebase_admin import auth

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"


def get_client():
    return auth


def get_user(uid):
    return auth.get_user(uid)
