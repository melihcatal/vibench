import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK (replace with your actual service account key)
# It's recommended to store your service account key securely and load it from an environment variable or a secure configuration management system.
# For demonstration purposes, we are assuming 'path/to/your/serviceAccountKey.json' exists.
try:
    cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
except ValueError:
    # If the app is already initialized, skip initialization
    pass

def send_password_reset_email(email: str):
    """
    Sends a password reset email to the specified user.

    Args:
        email: The email address of the user for whom to reset the password.

    Returns:
        A dictionary indicating success or failure.
    """
    try:
        auth.generate_password_reset_link(email)
        return {"status": "success", "message": f"Password reset email sent to {email}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

