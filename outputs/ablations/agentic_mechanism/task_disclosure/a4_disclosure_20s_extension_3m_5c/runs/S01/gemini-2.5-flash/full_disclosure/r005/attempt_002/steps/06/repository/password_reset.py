import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK (replace with your actual credentials)
# Make sure to set GOOGLE_APPLICATION_CREDENTIALS environment variable or provide the path to your service account key.
# For example: cred = credentials.Certificate("path/to/your/serviceAccountKey.json")
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def send_password_reset_email(email: str):
    """
    Sends a password reset email to the specified user using Firebase Authentication.
    """
    try:
        auth.generate_password_reset_link(email)
        return {"status": "success", "message": f"Password reset email sent to {email}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
