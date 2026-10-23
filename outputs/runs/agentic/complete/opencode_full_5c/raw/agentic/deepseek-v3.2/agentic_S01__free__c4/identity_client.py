import os
from typing import Dict, Any


def get_firebase_config() -> Dict[str, str]:
    """
    Load Firebase configuration from environment variables.
    """
    api_key = os.getenv("FIREBASE_API_KEY", "")
    project_id = os.getenv("FIREBASE_PROJECT_ID", "")

    if not api_key:
        raise ValueError("FIREBASE_API_KEY environment variable is required")
    if not project_id:
        raise ValueError("FIREBASE_PROJECT_ID environment variable is required")

    return {
        "api_key": api_key,
        "project_id": project_id,
        "auth_domain": f"{project_id}.firebaseapp.com",
    }


def validate_email(email: str) -> bool:
    """
    Validate email format.
    """
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password(password: str) -> bool:
    """
    Validate password meets minimum requirements.
    """
    if len(password) < 8:
        return False
    return True


def normalize_user_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize user data for consistency across API calls.
    """
    normalized = user_data.copy()

    # Ensure email is lowercase
    if "email" in normalized:
        normalized["email"] = normalized["email"].lower().strip()

    # Remove None values
    normalized = {k: v for k, v in normalized.items() if v is not None}

    return normalized
