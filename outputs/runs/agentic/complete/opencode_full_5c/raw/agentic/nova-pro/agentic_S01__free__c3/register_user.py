import firebase_admin
from firebase_admin import credentials, auth


def register_user(email, password):
    if not firebase_admin._apps:
        cred = credentials.Certificate("path/to/serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    user = auth.create_user(email=email, password=password)
    return user.uid
