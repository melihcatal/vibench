import os
from typing import Dict

import requests

from identity_models import OAuthConfig


def load_oauth_config() -> OAuthConfig:
    tenant_id = os.getenv("MICROSOFT_TENANT_ID", "common")
    authority = os.getenv("MICROSOFT_AUTHORITY", f"https://login.microsoftonline.com/{tenant_id}")
    return OAuthConfig(
        authority=authority,
        client_id=os.getenv("MICROSOFT_CLIENT_ID", ""),
        client_secret=os.getenv("MICROSOFT_CLIENT_SECRET", ""),
        redirect_uri=os.getenv("MICROSOFT_REDIRECT_URI", ""),
        tenant_id=tenant_id,
    )


def token_endpoint(config: OAuthConfig) -> str:
    return f"{config.authority}/oauth2/v2.0/token"


def authorize_endpoint(config: OAuthConfig) -> str:
    return f"{config.authority}/oauth2/v2.0/authorize"


def fetch_json(url: str, headers: Dict[str, str]) -> Dict:
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    return response.json()
