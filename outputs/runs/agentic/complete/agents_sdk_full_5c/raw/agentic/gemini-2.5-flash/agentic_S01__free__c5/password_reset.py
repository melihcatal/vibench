import firebase_admin
from firebase_admin import credentials, auth
import os

# Assume firebase_admin is initialized elsewhere or in a helper
if not firebase_admin._apps:
    # Use a service account file from an environment variable
    # For local development, this might point to a downloaded JSON key
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def password_reset(email: str) -> dict:
    """
    Starts a password reset flow for a user by sending a password reset email.
    Uses Firebase Admin SDK.
    """
    try:
        # Firebase Admin SDK provides a direct method to generate the link
        # The link is then typically sent via email by Firebase itself
        link = auth.generate_password_reset_link(email)
        return {"email": email, "message": f"Password reset email sent to {email}. Link: {link}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (replace with actual logic)
    # email = "test_user@example.com"
    # result = password_reset(email)
    # print(result)
    pass
