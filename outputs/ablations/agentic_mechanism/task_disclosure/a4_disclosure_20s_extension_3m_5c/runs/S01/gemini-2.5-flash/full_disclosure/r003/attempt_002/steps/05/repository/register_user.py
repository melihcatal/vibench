import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK (replace with your actual credentials)
# Make sure your serviceAccountKey.json is in a secure location and not exposed.
# For demonstration purposes, it's shown here, but in a real application,
# use environment variables or a more secure method to load credentials.
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

def register_user(email, password):
    """
    Creates a new email/password user account using Firebase Authentication.
    """
    try:
        user = auth.create_user(email=email, password=password)
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        raise Exception(f"Failed to register user: {e}")
