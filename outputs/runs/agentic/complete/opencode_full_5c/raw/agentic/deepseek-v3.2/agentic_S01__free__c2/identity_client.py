import os
import json
from typing import Dict, Any


def get_firebase_config() -> Dict[str, str]:
    """
    Load Firebase configuration from environment variables or config file.
    """
    config = {
        "api_key": os.environ.get("FIREBASE_API_KEY", ""),
        "project_id": os.environ.get("FIREBASE_PROJECT_ID", ""),
        "auth_domain": os.environ.get("FIREBASE_AUTH_DOMAIN", ""),
    }

    if not config["api_key"]:
        config_path = os.path.join(os.path.dirname(__file__), "firebase_config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                file_config = json.load(f)
                config.update(file_config)

    return config


def normalize_auth_response(response_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize authentication response from Firebase to a standard format.
    """
    return {
        "user_id": response_data.get("localId") or response_data.get("user_id"),
        "email": response_data.get("email"),
        "id_token": response_data.get("idToken") or response_data.get("id_token"),
        "refresh_token": response_data.get("refreshToken")
        or response_data.get("refresh_token"),
        "expires_in": response_data.get("expiresIn") or response_data.get("expires_in"),
    }


def validate_email(email: str) -> bool:
    """
    Basic email validation.
    """
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password(password: str) -> bool:
    """
    Basic password validation (at least 6 characters).
    """
    return len(password) >= 6
