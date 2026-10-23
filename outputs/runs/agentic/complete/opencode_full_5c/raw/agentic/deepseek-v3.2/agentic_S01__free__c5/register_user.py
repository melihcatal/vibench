import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
import os
from identity_client import get_firebase_client
from identity_models import UserRegistrationRequest, UserRegistrationResponse


def register_user(
    email: str, password: str, display_name: str = None
) -> UserRegistrationResponse:
    """Create a new email/password user account using Firebase Authentication."""
    try:
        # Initialize Firebase client
        firebase_app = get_firebase_client()

        # Create user with Firebase Authentication
        user_record = auth.create_user(
            email=email,
            password=password,
            display_name=display_name,
            email_verified=False,
        )

        # Generate custom token for the new user
        custom_token = auth.create_custom_token(user_record.uid)

        # Return normalized response
        return UserRegistrationResponse(
            user_id=user_record.uid,
            email=user_record.email,
            display_name=user_record.display_name,
            custom_token=custom_token.decode("utf-8")
            if isinstance(custom_token, bytes)
            else custom_token,
            provider="firebase",
            created_at=user_record.user_metadata.creation_timestamp.isoformat()
            if user_record.user_metadata.creation_timestamp
            else None,
        )
    except auth.EmailAlreadyExistsError:
        raise ValueError(f"User with email {email} already exists")
    except ValueError as e:
        raise ValueError(f"Invalid registration data: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Firebase registration failed: {str(e)}")
