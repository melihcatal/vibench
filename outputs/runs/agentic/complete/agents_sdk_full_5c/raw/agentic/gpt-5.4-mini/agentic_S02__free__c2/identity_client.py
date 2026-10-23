from __future__ import annotations

import base64
import hashlib
import os
import secrets
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests
from requests import Session

from identity_models import IdentityRequest, IdentityTokens, normalize_profile

OKTA_ISSUER_ENV = "OKTA_ISSUER"
OKTA_CLIENT_ID_ENV = "OKTA_CLIENT_ID"
OKTA_CLIENT_SECRET_ENV = "OKTA_CLIENT_SECRET"
OKTA_REDIRECT_URI_ENV = "OKTA_REDIRECT_URI"


class IdentityClient:
    def __init__(self, issuer: Optional[str] = None, client_id: Optional[str] = None, client_secret: Optional[str] = None, redirect_uri: Optional[str] = None, session: Optional[Session] = None) -> None:
        self.issuer = issuer or os.getenv(OKTA_ISSUER_ENV, "")
        self.client_id = client_id or os.getenv(OKTA_CLIENT_ID_ENV, "")
        self.client_secret = client_secret or os.getenv(OKTA_CLIENT_SECRET_ENV, "")
        self.redirect_uri = redirect_uri or os.getenv(OKTA_REDIRECT_URI_ENV, "")
        self.session = session or requests.Session()

    @property
    def discovery_url(self) -> str:
        return f"{self.issuer.rstrip('/')}/.well-known/openid-configuration"

    def discovery_document(self) -> Dict[str, Any]:
        return self.session.get(self.discovery_url, timeout=10).json()

    def authorization_url(self, scope: str = "openid profile email", state: Optional[str] = None, nonce: Optional[str] = None, code_challenge: Optional[str] = None, code_challenge_method: str = "S256") -> str:
        doc = self.discovery_document()
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "scope": scope,
            "redirect_uri": self.redirect_uri,
            "state": state or secrets.token_urlsafe(24),
            "nonce": nonce or secrets.token_urlsafe(24),
        }
        if code_challenge:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = code_challenge_method
        return f"{doc['authorization_endpoint']}?{urlencode(params)}"

    def exchange_code(self, code: str, code_verifier: Optional[str] = None) -> IdentityTokens:
        doc = self.discovery_document()
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
        }
        if self.client_secret:
            data["client_secret"] = self.client_secret
        if code_verifier:
            data["code_verifier"] = code_verifier
        resp = self.session.post(doc["token_endpoint"], data=data, timeout=10)
        resp.raise_for_status()
        payload = resp.json()
        return IdentityTokens(
            access_token=payload["access_token"],
            id_token=payload.get("id_token"),
            refresh_token=payload.get("refresh_token"),
            token_type=payload.get("token_type", "Bearer"),
            expires_in=payload.get("expires_in"),
            scope=payload.get("scope"),
            raw=payload,
        )

    def userinfo(self, access_token: str) -> Dict[str, Any]:
        doc = self.discovery_document()
        resp = self.session.get(doc["userinfo_endpoint"], headers={"Authorization": f"Bearer {access_token}"}, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def normalized_profile(self, access_token: str) -> Any:
        return normalize_profile(self.userinfo(access_token))


def generate_pkce_pair() -> Dict[str, str]:
    verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("ascii")
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode("ascii")
    return {"code_verifier": verifier, "code_challenge": challenge}


def build_identity_request(issuer: str, client_id: str, redirect_uri: str, scope: str = "openid profile email") -> IdentityRequest:
    return IdentityRequest(issuer=issuer, client_id=client_id, redirect_uri=redirect_uri, scope=scope)
