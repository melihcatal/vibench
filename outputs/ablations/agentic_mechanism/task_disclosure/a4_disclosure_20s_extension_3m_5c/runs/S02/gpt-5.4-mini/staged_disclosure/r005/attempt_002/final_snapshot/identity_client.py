import base64
import hashlib
import json
import os
import secrets
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class IdentityConfig:
    issuer_url: str
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    scope: str = "openid profile email"
    authorization_endpoint: Optional[str] = None
    token_endpoint: Optional[str] = None
    userinfo_endpoint: Optional[str] = None
    jwks_uri: Optional[str] = None


def load_identity_config(prefix: str = "FEDERATED_LOGIN") -> IdentityConfig:
    issuer_url = os.getenv(f"{prefix}_ISSUER_URL", "").strip()
    client_id = os.getenv(f"{prefix}_CLIENT_ID", "").strip()
    client_secret = os.getenv(f"{prefix}_CLIENT_SECRET")
    redirect_uri = os.getenv(f"{prefix}_REDIRECT_URI")
    scope = os.getenv(f"{prefix}_SCOPE", "openid profile email").strip()
    authorization_endpoint = os.getenv(f"{prefix}_AUTHORIZATION_ENDPOINT")
    token_endpoint = os.getenv(f"{prefix}_TOKEN_ENDPOINT")
    userinfo_endpoint = os.getenv(f"{prefix}_USERINFO_ENDPOINT")
    jwks_uri = os.getenv(f"{prefix}_JWKS_URI")
    if not issuer_url:
        raise ValueError("FEDERATED_LOGIN_ISSUER_URL is required")
    if not client_id:
        raise ValueError("FEDERATED_LOGIN_CLIENT_ID is required")
    return IdentityConfig(
        issuer_url=issuer_url,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        authorization_endpoint=authorization_endpoint,
        token_endpoint=token_endpoint,
        userinfo_endpoint=userinfo_endpoint,
        jwks_uri=jwks_uri,
    )


class FederatedLoginClient:
    def __init__(self, config: IdentityConfig, session: Optional[requests.Session] = None):
        self.config = config
        self.session = session or requests.Session()
        self._discovery_cache: Optional[Dict[str, Any]] = None

    def discover(self) -> Dict[str, Any]:
        if self._discovery_cache is None:
            url = self.config.issuer_url.rstrip("/") + "/.well-known/openid-configuration"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            self._discovery_cache = response.json()
        return self._discovery_cache

    @property
    def resolved_authorization_endpoint(self) -> str:
        return self.config.authorization_endpoint or self.discover()["authorization_endpoint"]

    @property
    def resolved_token_endpoint(self) -> str:
        return self.config.token_endpoint or self.discover()["token_endpoint"]

    @property
    def resolved_userinfo_endpoint(self) -> Optional[str]:
        return self.config.userinfo_endpoint or self.discover().get("userinfo_endpoint")

    def generate_pkce_pair(self) -> Dict[str, str]:
        verifier = self._b64url(secrets.token_bytes(32))
        challenge = self._b64url(hashlib.sha256(verifier.encode("ascii")).digest())
        return {"code_verifier": verifier, "code_challenge": challenge, "code_challenge_method": "S256"}

    def build_authorization_url(self, state: Optional[str] = None, nonce: Optional[str] = None) -> Dict[str, str]:
        state = state or self._b64url(secrets.token_bytes(16))
        nonce = nonce or self._b64url(secrets.token_bytes(16))
        pkce = self.generate_pkce_pair()
        params = {
            "response_type": "code",
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri or "",
            "scope": self.config.scope,
            "state": state,
            "nonce": nonce,
            **pkce,
        }
        query = "&".join(f"{self._quote(k)}={self._quote(v)}" for k, v in params.items() if v)
        return {"authorization_url": f"{self.resolved_authorization_endpoint}?{query}", "state": state, "nonce": nonce, **pkce}

    def exchange_code(self, code: str, code_verifier: str) -> Dict[str, Any]:
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.config.redirect_uri or "",
            "client_id": self.config.client_id,
            "code_verifier": code_verifier,
        }
        auth = None
        if self.config.client_secret:
            auth = (self.config.client_id, self.config.client_secret)
            data.pop("client_id", None)
        response = self.session.post(self.resolved_token_endpoint, data=data, auth=auth, timeout=15)
        response.raise_for_status()
        return response.json()

    def fetch_userinfo(self, access_token: str) -> Dict[str, Any]:
        if not self.resolved_userinfo_endpoint:
            raise RuntimeError("userinfo endpoint not available")
        response = self.session.get(
            self.resolved_userinfo_endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=15,
        )
        response.raise_for_status()
        return response.json()

    def token_is_expired(self, token_payload: Dict[str, Any], leeway_seconds: int = 30) -> bool:
        exp = token_payload.get("exp")
        if exp is None:
            return True
        return int(time.time()) >= int(exp) - leeway_seconds

    @staticmethod
    def _b64url(data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

    @staticmethod
    def _quote(value: str) -> str:
        return requests.utils.quote(value, safe="")


def create_identity_client(prefix: str = "FEDERATED_LOGIN") -> FederatedLoginClient:
    return FederatedLoginClient(load_identity_config(prefix=prefix))


def serialize_session(session_data: Dict[str, Any]) -> str:
    return json.dumps(session_data, separators=(",", ":"), sort_keys=True)


def deserialize_session(session_text: str) -> Dict[str, Any]:
    return json.loads(session_text)
