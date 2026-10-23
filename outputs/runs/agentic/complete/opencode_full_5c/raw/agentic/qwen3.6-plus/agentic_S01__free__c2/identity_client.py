import os
import json
import httpx
from typing import Optional, Dict, Any, Tuple
from urllib.parse import urlencode

FIREBASE_AUTH_BASE_URL = "https://identitytoolkit.googleapis.com/v1"
FIREBASE_AUTH_EMULATOR_URL = "http://localhost:9099/identitytoolkit.googleapis.com/v1"

FIREBASE_API_KEY_ENV = "FIREBASE_API_KEY"
FIREBASE_PROJECT_ID_ENV = "FIREBASE_PROJECT_ID"
FIREBASE_CREDENTIALS_ENV = "FIREBASE_CREDENTIALS"
FIREBASE_USE_EMULATOR_ENV = "FIREBASE_USE_EMULATOR"


class IdentityConfig:
    def __init__(
        self,
        api_key: Optional[str] = None,
        project_id: Optional[str] = None,
        use_emulator: bool = False,
    ):
        self.api_key = api_key or os.environ.get(FIREBASE_API_KEY_ENV, "")
        self.project_id = project_id or os.environ.get(FIREBASE_PROJECT_ID_ENV, "")
        self.use_emulator = use_emulator or os.environ.get(
            FIREBASE_USE_EMULATOR_ENV, ""
        ).lower() in ("true", "1", "yes")

    @property
    def base_url(self) -> str:
        if self.use_emulator:
            return FIREBASE_AUTH_EMULATOR_URL
        return FIREBASE_AUTH_BASE_URL

    def is_valid(self) -> bool:
        return bool(self.api_key) and bool(self.project_id)

    def get_auth_url(self, endpoint: str) -> str:
        base = self.base_url.rstrip("/")
        endpoint = endpoint.lstrip("/")
        return f"{base}/{endpoint}?key={self.api_key}"


def load_config() -> IdentityConfig:
    return IdentityConfig()


def load_firebase_credentials() -> Optional[Dict[str, Any]]:
    creds_path = os.environ.get(FIREBASE_CREDENTIALS_ENV)
    if creds_path and os.path.isfile(creds_path):
        with open(creds_path, "r") as f:
            return json.load(f)
    creds_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")
    if creds_json:
        return json.loads(creds_json)
    return None


async def make_firebase_request(
    config: IdentityConfig,
    endpoint: str,
    method: str = "POST",
    payload: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
) -> Tuple[int, Dict[str, Any]]:
    url = config.get_auth_url(endpoint)
    request_headers = {"Content-Type": "application/json"}
    if headers:
        request_headers.update(headers)

    async with httpx.AsyncClient(timeout=30.0) as client:
        if method.upper() == "POST":
            response = await client.post(url, json=payload, headers=request_headers)
        elif method.upper() == "GET":
            response = await client.get(url, headers=request_headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        try:
            data = response.json()
        except Exception:
            data = {"raw": response.text}

        return response.status_code, data


async def verify_id_token(config: IdentityConfig, id_token: str) -> Dict[str, Any]:
    url = f"https://identitytoolkit.googleapis.com/v1/token:lookup?key={config.api_key}"
    payload = {"idToken": id_token}

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()


def build_custom_token_payload(
    uid: str,
    custom_claims: Optional[Dict[str, Any]] = None,
    ttl_seconds: int = 3600,
) -> Dict[str, Any]:
    payload = {
        "uid": uid,
        "claims": custom_claims or {},
        "ttl": f"{ttl_seconds}s",
    }
    return payload


def extract_user_info(firebase_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "uid": firebase_data.get("localId", ""),
        "email": firebase_data.get("email", ""),
        "display_name": firebase_data.get("displayName"),
        "email_verified": firebase_data.get("emailVerified", False),
        "photo_url": firebase_data.get("photoUrl"),
        "created_at": firebase_data.get("createdAt"),
        "last_login_at": firebase_data.get("lastLoginAt"),
        "provider_data": firebase_data.get("providerUserInfo", []),
    }


def format_firebase_error(
    status_code: int, error_data: Dict[str, Any]
) -> Dict[str, Any]:
    error_info = error_data.get("error", {})
    return {
        "status_code": status_code,
        "error_code": error_info.get("code", status_code),
        "message": error_info.get("message", "Unknown Firebase Auth error"),
        "errors": error_info.get("errors", []),
    }
