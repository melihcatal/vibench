import os
import firebase_admin
from firebase_admin import auth
from identity_client import get_firebase_app

def password_reset(email):
    """
    Starts a password reset flow for a local account by sending a password reset email.
    """
    app = get_firebase_app()
    try:
        auth.generate_password_reset_link(email)
        return {"email": email, "message": "Password reset email sent successfully"}
    except auth.UserNotFoundError:
        return {"error": "User not found with this email"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (requires Firebase project setup and credentials)
    # Ensure FIREBASE_CREDENTIALS_PATH environment variable is set
    # result = password_reset("test@example.com")
    # print(result)
    pass
