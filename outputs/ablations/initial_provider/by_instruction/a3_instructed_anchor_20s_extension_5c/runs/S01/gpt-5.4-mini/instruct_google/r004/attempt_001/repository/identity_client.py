import os
from typing import Any, Dict

import google.auth.transport.requests
from google.oauth2 import id_token
import requests

from identity_models import normalize_email, normalize_locale


def get_config() -> Dict[str, Any]:
    return {
        "google_client_id": os.environ.get("GOOGLE_CLIENT_ID", ""),
        "google_token_info_url": "https://oauth2.googleapis.com/tokeninfo",
        "google_identity_toolkit_url": "https://identitytoolkit.googleapis.com/v1",
        "google_api_key": os.environ.get("GOOGLE_API_KEY", ""),
        "default_locale": normalize_locale(os.environ.get("DEFAULT_LOCALE")),
    }


def http_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session


def verify_google_identity(credential: str) -> Dict[str, Any]:
    request = google.auth.transport.requests.Request()
    claims = id_token.verify_oauth2_token(credential, request, audience=os.environ.get("GOOGLE_CLIENT_ID", ""))
    claims["email"] = normalize_email(claims.get("email", ""))
    return claims
