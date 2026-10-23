import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
import os

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def email_password_login(email, password):
    """
    Simulates email/password login by creating a custom token for the user.
    Note: Direct email/password login is typically handled by client SDKs.
    This server-side function demonstrates interaction by verifying user existence
    and then generating a custom token that a client can use to sign in.
    """
    try:
        user = auth.get_user_by_email(email)
        # In a real scenario, password verification would happen client-side
        # or via a Firebase Authentication REST API call.
        # Here, we assume the user exists and generate a custom token.
        custom_token = auth.create_custom_token(user.uid)
        return {"uid": user.uid, "custom_token": custom_token.decode('utf-8'), "message": "Custom token generated for user"}
    except auth.UserNotFoundError:
        return {"error": "User not found"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage
    user_email = os.environ.get("TEST_USER_EMAIL", "test@example.com")
    user_password = os.environ.get("TEST_USER_PASSWORD", "SuperSecurePassword123!") # Not used directly here, but for context

    result = email_password_login(user_email, user_password)
    print(result)
