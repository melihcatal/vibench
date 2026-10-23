import os
from firebase_admin import auth, initialize_app, credentials
from identity_client import get_firebase_app


def register_user(email: str, password: str, display_name: str = None) -> dict:
    """Create a new email/password user account using Firebase Authentication."""
    app = get_firebase_app()

    try:
        user_record = auth.create_user(
            app=app,
            email=email,
            password=password,
            display_name=display_name,
            email_verified=False,
        )

        return {
            "user_id": user_record.uid,
            "email": user_record.email,
            "display_name": user_record.display_name,
            "created_at": user_record.user_metadata.creation_timestamp,
            "provider": "firebase",
        }
    except auth.EmailAlreadyExistsError:
        raise ValueError(f"User with email {email} already exists")
    except ValueError as e:
        raise ValueError(f"Invalid input: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Firebase authentication error: {str(e)}")
