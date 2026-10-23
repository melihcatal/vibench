import os
from typing import Any, Dict

from google.auth.transport.requests import Request
from google.oauth2 import id_token

from identity_models import AccountRequest, TokenResponse


GOOGLE_IDENTITY_ISSUER = "https://accounts.google.com"


def get_project_id() -> str:
    return os.getenv("GOOGLE_CLOUD_PROJECT", "")


def get_api_key() -> str:
    return os.getenv("FIREBASE_WEB_API_KEY", "")


def verify_google_id_token(token: str) -> Dict[str, Any]:
    claims = id_token.verify_oauth2_token(token, Request(), GOOGLE_IDENTITY_ISSUER)
    return claims


def build_account_request(email: str, password: str = None, locale: str = None) -> AccountRequest:
    return AccountRequest(email=email, password=password, locale=locale)


def tokens_from_response(payload: Dict[str, Any]) -> TokenResponse:
    return TokenResponse.from_dict(payload)


def require_api_key() -> str:
    key = get_api_key()
    if not key:
        raise RuntimeError("FIREBASE_WEB_API_KEY is required")
    return key
