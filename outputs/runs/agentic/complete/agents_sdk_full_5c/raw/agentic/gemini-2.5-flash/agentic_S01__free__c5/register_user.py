import firebase_admin
from firebase_admin import credentials, auth
import os

# Assume firebase_admin is initialized elsewhere or in a helper
# For demonstration, we'll initialize here if not already.
# In a real app, identity_client.py would handle this.
if not firebase_admin._apps:
    # Use a service account file from an environment variable
    # For local development, this might point to a downloaded JSON key
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred)

def register_user(email: str, password: str) -> dict:
    """
    Registers a new user with email and password using Firebase Authentication.
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
    # Example usage (replace with actual logic)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for local testing
    # result = register_user("test_user@example.com", "SecurePassword123!")
    # print(result)
    pass
