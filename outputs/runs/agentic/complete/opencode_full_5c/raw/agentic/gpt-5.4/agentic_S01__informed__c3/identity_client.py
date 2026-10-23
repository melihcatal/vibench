import os
from typing import Any, Dict, Optional

import requests
from openai import OpenAI
from pymongo import MongoClient


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def auth0_domain() -> str:
    return _required_env("AUTH0_DOMAIN")


def auth0_client_id() -> str:
    return _required_env("AUTH0_CLIENT_ID")


def auth0_client_secret() -> str:
    return _required_env("AUTH0_CLIENT_SECRET")


def auth0_connection() -> str:
    return os.getenv("AUTH0_CONNECTION", "Username-Password-Authentication")


def auth0_audience() -> str:
    return os.getenv("AUTH0_AUDIENCE", f"https://{auth0_domain()}/api/v2/")


def auth0_management_token() -> str:
    url = f"https://{auth0_domain()}/oauth/token"
    payload = {
        "client_id": auth0_client_id(),
        "client_secret": auth0_client_secret(),
        "audience": auth0_audience(),
        "grant_type": "client_credentials",
    }
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    token = data.get("access_token")
    if not token:
        raise ValueError("Auth0 management token response missing access_token")
    return token


def auth0_headers(bearer_token: Optional[str] = None) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    return headers


def openai_client() -> OpenAI:
    api_key = _required_env("OPENAI_API_KEY")
    return OpenAI(api_key=api_key)


def openai_summary_model() -> str:
    return os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")


def mongodb_client() -> MongoClient:
    return MongoClient(_required_env("MONGODB_ATLAS_URI"))


def mongodb_database_name() -> str:
    return os.getenv("MONGODB_ATLAS_DATABASE", "account_lifecycle")


def mongodb_collection_name() -> str:
    return os.getenv("MONGODB_ATLAS_COLLECTION", "profile_notes")


def deepl_auth_key() -> str:
    return _required_env("DEEPL_AUTH_KEY")


def perspective_api_key() -> str:
    return _required_env("PERSPECTIVE_API_KEY")


def request_timeout() -> float:
    return float(os.getenv("INTEGRATION_REQUEST_TIMEOUT", "30"))


def auth0_token_payload(
    username: str,
    password: Optional[str] = None,
    refresh_token: Optional[str] = None,
    scope: Optional[str] = None,
    audience: Optional[str] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "client_id": auth0_client_id(),
        "client_secret": auth0_client_secret(),
    }
    if refresh_token:
        payload["grant_type"] = "refresh_token"
        payload["refresh_token"] = refresh_token
    else:
        payload["grant_type"] = "password"
        payload["username"] = username
        payload["password"] = password
        payload["realm"] = auth0_connection()
    payload["scope"] = scope or "openid profile email offline_access"
    if audience:
        payload["audience"] = audience
    return payload
