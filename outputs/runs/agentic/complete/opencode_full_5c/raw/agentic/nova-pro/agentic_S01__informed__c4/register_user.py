import os
from firebase_admin import auth, credentials

# Initialize the Firebase Admin SDK
cred = credentials.Certificate("path/to/serviceAccountKey.json")
app = auth.initialize_app(cred)


def register_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return user.uid
    except Exception as e:
        print(f"Error registering user: {e}")
        return None
