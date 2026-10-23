import os
from typing import Dict, Any


def get_identity_config() -> Dict[str, Any]:
    return {
        "auth0_domain": os.getenv("AUTH0_DOMAIN"),
        "auth0_client_id": os.getenv("AUTH0_CLIENT_ID"),
        "auth0_client_secret": os.getenv("AUTH0_CLIENT_SECRET")
    }


def validate_identity_config() -> bool:
    required_keys = ["AUTH0_DOMAIN", "AUTH0_CLIENT_ID"]
    return all(os.getenv(key) for key in required_keys)