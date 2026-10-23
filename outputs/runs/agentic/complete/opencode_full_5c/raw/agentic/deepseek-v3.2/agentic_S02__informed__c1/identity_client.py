import os
import json
from typing import Dict, Any, Optional


def get_oauth_config() -> Dict[str, str]:
    return {
        "domain": os.environ.get("AUTH0_DOMAIN", ""),
        "client_id": os.environ.get("AUTH0_CLIENT_ID", ""),
        "client_secret": os.environ.get("AUTH0_CLIENT_SECRET", ""),
        "audience": os.environ.get("AUTH0_AUDIENCE", ""),
        "issuer": f"https://{os.environ.get('AUTH0_DOMAIN', '')}/",
    }


def validate_oauth_config(config: Dict[str, str]) -> bool:
    required_keys = ["domain", "client_id", "client_secret"]
    for key in required_keys:
        if not config.get(key):
            return False
    return True


def build_redirect_uri(base_url: str, path: str = "/callback") -> str:
    return f"{base_url.rstrip('/')}{path}"


def parse_id_token(id_token: str) -> Dict[str, Any]:
    import jwt

    config = get_oauth_config()

    try:
        decoded = jwt.decode(id_token, options={"verify_signature": False})
        return decoded
    except Exception as e:
        raise ValueError(f"Failed to parse ID token: {e}")


def normalize_scope(scope: str) -> str:
    scopes = set(scope.split())
    if "openid" not in scopes:
        scopes.add("openid")
    if "profile" not in scopes:
        scopes.add("profile")
    if "email" not in scopes:
        scopes.add("email")
    return " ".join(sorted(scopes))
