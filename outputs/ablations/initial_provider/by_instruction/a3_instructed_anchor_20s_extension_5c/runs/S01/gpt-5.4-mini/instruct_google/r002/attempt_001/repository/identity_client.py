import os
from typing import Any, Dict, Optional


def get_identity_config() -> Dict[str, str]:
    return {
        "google_identity_platform_api_key": os.getenv("GOOGLE_IDENTITY_PLATFORM_API_KEY", ""),
        "google_identity_platform_project_id": os.getenv("GOOGLE_CLOUD_PROJECT", ""),
        "google_identity_platform_auth_url": os.getenv(
            "GOOGLE_IDENTITY_PLATFORM_AUTH_URL",
            "https://identitytoolkit.googleapis.com/v1",
        ),
    }


def auth_endpoint(path: str) -> str:
    base = get_identity_config()["google_identity_platform_auth_url"].rstrip("/")
    return f"{base}/{path.lstrip('/')}"


def auth_params() -> Dict[str, str]:
    api_key = get_identity_config()["google_identity_platform_api_key"]
    return {"key": api_key} if api_key else {}


def parse_json_response(payload: Dict[str, Any]) -> Dict[str, Any]:
    return dict(payload)


def build_headers(id_token: Optional[str] = None) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if id_token:
        headers["Authorization"] = f"Bearer {id_token}"
    return headers
