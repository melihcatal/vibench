import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class IdentityConfig:
    issuer_url: str
    client_id: str
    client_secret: str
    redirect_uri: str
    scope: str = "openid profile email"


def load_identity_config(prefix: str = "FEDERATED_LOGIN_") -> IdentityConfig:
    issuer_url = os.getenv(f"{prefix}ISSUER_URL", "").strip()
    client_id = os.getenv(f"{prefix}CLIENT_ID", "").strip()
    client_secret = os.getenv(f"{prefix}CLIENT_SECRET", "").strip()
    redirect_uri = os.getenv(f"{prefix}REDIRECT_URI", "").strip()
    scope = os.getenv(f"{prefix}SCOPE", "openid profile email").strip()

    missing = [
        name
        for name, value in (
            ("issuer_url", issuer_url),
            ("client_id", client_id),
            ("client_secret", client_secret),
            ("redirect_uri", redirect_uri),
        )
        if not value
    ]
    if missing:
        raise ValueError(f"Missing identity configuration: {', '.join(missing)}")

    return IdentityConfig(
        issuer_url=issuer_url.rstrip("/"),
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
    )


class FederatedLoginClient:
    def __init__(self, config: Optional[IdentityConfig] = None, timeout: int = 15):
        self.config = config or load_identity_config()
        self.timeout = timeout

    def discovery_document(self) -> Dict[str, Any]:
        url = f"{self.config.issuer_url}/.well-known/openid-configuration"
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def authorization_url(self, state: str, nonce: Optional[str] = None, code_challenge: Optional[str] = None, code_challenge_method: Optional[str] = None) -> str:
        doc = self.discovery_document()
        endpoint = doc["authorization_endpoint"]
        params = {
            "response_type": "code",
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "scope": self.config.scope,
            "state": state,
        }
        if nonce:
            params["nonce"] = nonce
        if code_challenge:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = code_challenge_method or "S256"
        return requests.Request("GET", endpoint, params=params).prepare().url

    def exchange_code(self, code: str) -> Dict[str, Any]:
        doc = self.discovery_document()
        token_endpoint = doc["token_endpoint"]
        response = requests.post(
            token_endpoint,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.config.redirect_uri,
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        doc = self.discovery_document()
        token_endpoint = doc["token_endpoint"]
        response = requests.post(
            token_endpoint,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def userinfo(self, access_token: str) -> Dict[str, Any]:
        doc = self.discovery_document()
        userinfo_endpoint = doc.get("userinfo_endpoint")
        if not userinfo_endpoint:
            raise ValueError("Issuer does not advertise a userinfo endpoint")
        response = requests.get(
            userinfo_endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()
