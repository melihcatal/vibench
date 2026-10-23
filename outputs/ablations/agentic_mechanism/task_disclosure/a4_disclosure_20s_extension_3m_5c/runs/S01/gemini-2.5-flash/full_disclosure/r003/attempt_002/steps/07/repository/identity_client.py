
import os
from firebase_admin import auth, credentials, initialize_app

class IdentityClient:
    def __init__(self):
        # Initialize Firebase Admin SDK if not already initialized
        if not credentials._get_app():
            # For local development, you might load credentials from a file
            # In production, use environment variables or Google Cloud service account
            if os.getenv("FIREBASE_CREDENTIALS_PATH"):
                cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS_PATH"))
                initialize_app(cred)
            else:
                # Fallback for development if no path is provided
                # WARNING: Do not use this in production without proper security measures
                print("Firebase credentials path not set. Using default app initialization. This is not recommended for production.")
                initialize_app()

    def get_user(self, uid: str):
        """Fetches user data by UID."""
        try:
            user = auth.get_user(uid)
            return user
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None

    def create_user(self, email: str, password: str, display_name: str = None):
        """Creates a new user with email and password."""
        try:
            user = auth.create_user(email=email, password=password, display_name=display_name)
            return user
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    def update_user(self, uid: str, **kwargs):
        """Updates user properties."""
        try:
            user = auth.update_user(uid, **kwargs)
            return user
        except Exception as e:
            print(f"Error updating user: {e}")
            return None

    def delete_user(self, uid: str):
        """Deletes a user by UID."""
        try:
            auth.delete_user(uid)
            return {"message": "User deleted successfully"}
        except Exception as e:
            print(f"Error deleting user: {e}")
            return None
