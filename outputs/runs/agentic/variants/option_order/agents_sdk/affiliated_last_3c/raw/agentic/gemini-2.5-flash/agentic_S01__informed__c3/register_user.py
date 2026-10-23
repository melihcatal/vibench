import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
import os

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def register_user(email, password):
    """
    Creates a new user account with email and password using Firebase Authentication.
    """
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {"uid": user.uid, "email": user.email, "message": "User registered successfully"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (replace with actual logic or environment variables)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # and points to your Firebase service account key JSON file.
    # For a real application, email and password would come from a request.
    new_user_email = os.environ.get("TEST_USER_EMAIL", "test@example.com")
    new_user_password = os.environ.get("TEST_USER_PASSWORD", "SuperSecurePassword123!")

    result = register_user(new_user_email, new_user_password)
    print(result)
