import os
import firebase_admin
from firebase_admin import credentials
from typing import Optional

# Firebase configuration
FIREBASE_CREDENTIALS_PATH = os.environ.get(
    "FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json"
)
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID")
FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY")

# Singleton Firebase app instance
_firebase_app = None


def get_firebase_client():
    """Initialize and return Firebase Admin SDK client."""
    global _firebase_app

    if _firebase_app is None:
        try:
            # Check for credentials
            if os.path.exists(FIREBASE_CREDENTIALS_PATH):
                cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            else:
                # Try to use default credentials (e.g., from environment)
                cred = credentials.ApplicationDefault()

            # Initialize Firebase app
            _firebase_app = firebase_admin.initialize_app(
                cred,
                name="identity-service",
                options={
                    "projectId": FIREBASE_PROJECT_ID,
                }
                if FIREBASE_PROJECT_ID
                else {},
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Firebase client: {str(e)}")

    return _firebase_app


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


def normalize_user_data(email: str, display_name: Optional[str] = None) -> dict:
    """Normalize user data for consistency."""
    normalized = {
        "email": email.strip().lower(),
        "display_name": display_name.strip() if display_name else None,
    }
    return normalized


def get_provider_config() -> dict:
    """Get provider configuration."""
    return {
        "provider": "firebase",
        "project_id": FIREBASE_PROJECT_ID,
        "api_key_configured": bool(FIREBASE_API_KEY),
        "credentials_configured": os.path.exists(FIREBASE_CREDENTIALS_PATH)
        or FIREBASE_PROJECT_ID is not None,
    }
