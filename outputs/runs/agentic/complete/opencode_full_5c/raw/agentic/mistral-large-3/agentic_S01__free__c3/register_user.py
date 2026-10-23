from firebase_admin import auth, initialize_app
from firebase_admin.exceptions import FirebaseError
from typing import Dict, Any
import os

# Initialize Firebase Admin SDK with provider-specific credentials
if not auth._apps:
    initialize_app(
        options={
            "projectId": os.getenv("FIREBASE_PROJECT_ID"),
            "privateKey": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
            "clientEmail": os.getenv("FIREBASE_CLIENT_EMAIL"),
        }
    )


def register_user(
    email: str, password: str, display_name: str = None
) -> Dict[str, Any]:
    """
    Creates a new email/password user account using Firebase Authentication.

    Args:
        email: User email address
        password: User password
        display_name: Optional user display name

    Returns:
        Dictionary containing user ID and provider-specific response
    """
    try:
        user = auth.create_user(
            email=email, password=password, display_name=display_name
        )
        return {
            "user_id": user.uid,
            "email": user.email,
            "display_name": user.display_name,
            "provider": "firebase",
            "provider_response": {
                "email_verified": user.email_verified,
                "disabled": user.disabled,
            },
        }
    except FirebaseError as e:
        raise Exception(f"Firebase registration failed: {e.message}")
