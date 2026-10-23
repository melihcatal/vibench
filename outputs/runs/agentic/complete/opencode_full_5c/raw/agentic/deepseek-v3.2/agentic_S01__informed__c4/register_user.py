import os
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials


def register_user(email: str, password: str, display_name: str = None) -> dict:
    """
    Register a new user with email and password using Firebase Authentication.
    """
    if not firebase_admin._apps:
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not cred_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            )
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

    try:
        user_record = auth.create_user(
            email=email,
            password=password,
            display_name=display_name,
            email_verified=False,
        )

        return {
            "user_id": user_record.uid,
            "email": user_record.email,
            "display_name": user_record.display_name,
            "email_verified": user_record.email_verified,
            "created_at": user_record.user_metadata.creation_timestamp,
            "provider": "firebase",
        }
    except auth.EmailAlreadyExistsError:
        raise ValueError("Email already exists")
    except Exception as e:
        raise RuntimeError(f"Failed to create user: {str(e)}")
