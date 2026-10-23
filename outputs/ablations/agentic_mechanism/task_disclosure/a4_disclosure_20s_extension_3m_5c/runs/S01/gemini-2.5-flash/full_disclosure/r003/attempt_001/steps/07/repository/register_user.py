import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK (replace with your service account key file)
# It's recommended to set the path to your service account key file using an environment variable
# e.g., GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/serviceAccountKey.json"
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def register_user(email, password):
    """
    Creates a new email/password user account using Firebase Authentication.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        dict: A dictionary containing the user's UID and email, or an error message.
    """
    try:
        user = auth.create_user(email=email, password=password)
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        return {"error": str(e)}
