import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK (replace with your actual credentials)
# It's recommended to load credentials from an environment variable or a secure configuration system
# For demonstration purposes, a placeholder is used.
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

def register_user(email, password):
    """
    Creates a new email/password user account using Firebase Authentication.

    Args:
        email (str): The user's email address.
        password (str): The user's desired password.

    Returns:
        dict: A dictionary containing user information on success, or an error message.
    """
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {"uid": user.uid, "email": user.email, "message": "User registered successfully"}
    except Exception as e:
        return {"error": str(e)}

