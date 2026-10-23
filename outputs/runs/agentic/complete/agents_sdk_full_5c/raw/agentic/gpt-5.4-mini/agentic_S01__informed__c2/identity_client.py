from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import requests

from identity_models import normalize_email, normalize_locale


@dataclass(frozen=True)
class IdentityConfig:
    auth0_domain: str
    auth0_client_id: str
    auth0_client_secret: Optional[str]
    management_audience: str
    content_safety_endpoint: Optional[str]
    content_safety_key: Optional[str]
    translator_endpoint: Optional[str]
    translator_key: Optional[str]
    translator_region: Optional[str]
    document_store_url: Optional[str]
    document_store_apikey: Optional[str]


@lru_cache(maxsize=1)
def load_config() -> IdentityConfig:
    return IdentityConfig(
        auth0_domain=os.environ.get("AUTH0_DOMAIN", ""),
        auth0_client_id=os.environ.get("AUTH0_CLIENT_ID", ""),
        auth0_client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
        management_audience=os.environ.get("AUTH0_MANAGEMENT_AUDIENCE", f"https://{os.environ.get('AUTH0_DOMAIN', '')}/api/v2/"),
        content_safety_endpoint=os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT"),
        content_safety_key=os.environ.get("AZURE_CONTENT_SAFETY_KEY"),
        translator_endpoint=os.environ.get("AZURE_TRANSLATOR_ENDPOINT"),
        translator_key=os.environ.get("AZURE_TRANSLATOR_KEY"),
        translator_region=os.environ.get("AZURE_TRANSLATOR_REGION"),
        document_store_url=os.environ.get("IBM_CLOUDANT_URL"),
        document_store_apikey=os.environ.get("IBM_CLOUDANT_APIKEY"),
    )


class Auth0RestClient:
    def __init__(self, config: Optional[IdentityConfig] = None) -> None:
        self.config = config or load_config()
        if not self.config.auth0_domain:
            raise ValueError("AUTH0_DOMAIN is required")
        self.base_url = f"https://{self.config.auth0_domain}"

    def _headers(self, token: Optional[str] = None) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def token(self, grant_type: str, **data: Any) -> Dict[str, Any]:
        body = {
            "grant_type": grant_type,
            "client_id": self.config.auth0_client_id,
            **data,
        }
        if self.config.auth0_client_secret:
            body["client_secret"] = self.config.auth0_client_secret
        response = requests.post(f"{self.base_url}/oauth/token", json=body, headers=self._headers())
        response.raise_for_status()
        return response.json()

    def management_request(self, method: str, path: str, access_token: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = requests.request(method, f"{self.base_url}{path}", headers=self._headers(access_token), json=json)
        response.raise_for_status()
        if response.text:
            return response.json()
        return {}


@lru_cache(maxsize=1)
def get_client() -> Auth0RestClient:
    return Auth0RestClient()


def build_user_payload(email: str, password: str, locale: Optional[str] = None, display_name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "email": normalize_email(email),
        "password": password,
        "connection": "Username-Password-Authentication",
        "email_verified": False,
        "verify_email": True,
        "user_metadata": metadata or {},
    }
    if display_name:
        payload["name"] = display_name
    if locale:
        payload["user_metadata"]["locale"] = normalize_locale(locale)
    return payload
