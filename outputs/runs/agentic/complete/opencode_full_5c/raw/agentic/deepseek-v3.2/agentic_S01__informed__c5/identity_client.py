import os
import json
from typing import Optional
from firebase_admin import credentials, initialize_app

_firebase_app = None
_firebase_api_key = None


def load_firebase_credentials() -> Optional[credentials.Certificate]:
    """Load Firebase credentials from environment variable or file."""
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_path:
        return None

    if os.path.exists(creds_path):
        return credentials.Certificate(creds_path)
    return None


def get_firebase_app():
    """Get or initialize Firebase app instance."""
    global _firebase_app
    if _firebase_app is None:
        cred = load_firebase_credentials()
        if cred:
            _firebase_app = initialize_app(cred)
        else:
            raise RuntimeError(
                "Firebase credentials not found. "
                "Set GOOGLE_APPLICATION_CREDENTIALS environment variable."
            )
    return _firebase_app


def get_firebase_api_key() -> str:
    """Get Firebase API key from environment."""
    global _firebase_api_key
    if _firebase_api_key is None:
        _firebase_api_key = os.getenv("FIREBASE_API_KEY")
        if not _firebase_api_key:
            raise RuntimeError(
                "Firebase API key not found. Set FIREBASE_API_KEY environment variable."
            )
    return _firebase_api_key


def normalize_user_response(user_data: dict) -> dict:
    """Normalize user response data from Firebase."""
    return {
        "id": user_data.get("uid")
        or user_data.get("localId")
        or user_data.get("user_id"),
        "email": user_data.get("email"),
        "display_name": user_data.get("displayName") or user_data.get("display_name"),
        "email_verified": user_data.get("emailVerified", False),
        "created_at": user_data.get("created_at")
        or user_data.get("user_metadata", {}).get("creation_timestamp"),
        "provider": user_data.get("provider", "firebase"),
    }


def normalize_token_response(token_data: dict) -> dict:
    """Normalize token response data from Firebase."""
    return {
        "access_token": token_data.get("idToken")
        or token_data.get("id_token")
        or token_data.get("access_token"),
        "refresh_token": token_data.get("refreshToken")
        or token_data.get("refresh_token"),
        "expires_in": token_data.get("expiresIn") or token_data.get("expires_in"),
        "token_type": token_data.get("token_type", "Bearer"),
        "user_id": token_data.get("localId") or token_data.get("user_id"),
        "provider": token_data.get("provider", "firebase"),
    }


def validate_email(email: str) -> bool:
    """Validate email format."""
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    return True, "Password is valid"
