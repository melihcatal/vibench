import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
import os

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def password_reset(email):
    """
    Starts a password reset flow for a Firebase account by sending a reset email.
    """
    try:
        auth.generate_password_reset_link(email)
        return {"message": f"Password reset email sent to {email}"}
    except auth.UserNotFoundError:
        return {"error": "User not found with this email."}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage
    user_email_for_reset = os.environ.get("TEST_USER_EMAIL_FOR_RESET", "reset@example.com")

    result = password_reset(user_email_for_reset)
    print(result)
