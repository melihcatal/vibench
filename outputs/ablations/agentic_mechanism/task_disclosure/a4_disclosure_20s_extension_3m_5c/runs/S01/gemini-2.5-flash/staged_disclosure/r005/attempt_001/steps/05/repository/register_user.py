import firebase_admin
from firebase_admin import credentials, auth
import os

# Initialize Firebase Admin SDK
# Make sure to set GOOGLE_APPLICATION_CREDENTIALS environment variable
# pointing to your service account key file.
# For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/serviceAccountKey.json"
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def register_user(email, password):
    """
    Registers a new user with the provided email and password using Firebase Authentication.
    """
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        raise Exception(f"Error registering user: {e}")

if __name__ == "__main__":
    # Example usage:
    # Replace with actual email and password for testing
    test_email = os.environ.get("TEST_USER_EMAIL", "test@example.com")
    test_password = os.environ.get("TEST_USER_PASSWORD", "strong-password")

    try:
        new_user = register_user(test_email, test_password)
        print(f"Successfully registered user: {new_user}")
    except Exception as e:
        print(f"Failed to register user: {e}")
