import base64
import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class IdentityClientConfig:
    issuer_url: str
    client_id: str
    client_secret: str
    redirect_uri: str
    token_endpoint: str
    authorization_endpoint: str
    jwks_url: str
    scope: str = "openid profile email"


def load_identity_config() -> IdentityClientConfig:
    issuer_url = os.environ["FEDERATED_LOGIN_ISSUER_URL"].rstrip("/")
    client_id = os.environ["FEDERATED_LOGIN_CLIENT_ID"]
    client_secret = os.environ["FEDERATED_LOGIN_CLIENT_SECRET"]
    redirect_uri = os.environ["FEDERATED_LOGIN_REDIRECT_URI"]

    discovery_url = f"{issuer_url}/.well-known/openid-configuration"
    discovery = requests.get(discovery_url, timeout=10).json()

    return IdentityClientConfig(
        issuer_url=issuer_url,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        token_endpoint=discovery["token_endpoint"],
        authorization_endpoint=discovery["authorization_endpoint"],
        jwks_url=discovery["jwks_uri"],
        scope=os.getenv("FEDERATED_LOGIN_SCOPE", "openid profile email"),
    )


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_pkce_pair() -> Dict[str, str]:
    verifier = _b64url(os.urandom(32))
    challenge = _b64url(hashlib.sha256(verifier.encode("ascii")).digest())
    return {"code_verifier": verifier, "code_challenge": challenge}


def build_authorization_url(config: IdentityClientConfig, state: str, nonce: str, code_challenge: str) -> str:
    from urllib.parse import urlencode

    query = urlencode(
        {
            "response_type": "code",
            "client_id": config.client_id,
            "redirect_uri": config.redirect_uri,
            "scope": config.scope,
            "state": state,
            "nonce": nonce,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
    )
    return f"{config.authorization_endpoint}?{query}"


def exchange_code_for_tokens(config: IdentityClientConfig, code: str, code_verifier: str) -> Dict[str, Any]:
    response = requests.post(
        config.token_endpoint,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": config.redirect_uri,
            "client_id": config.client_id,
            "client_secret": config.client_secret,
            "code_verifier": code_verifier,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def refresh_access_token(config: IdentityClientConfig, refresh_token: str) -> Dict[str, Any]:
    response = requests.post(
        config.token_endpoint,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": config.client_id,
            "client_secret": config.client_secret,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def verify_id_token_signature(id_token: str, jwk: Dict[str, Any], expected_issuer: str, expected_audience: str) -> Dict[str, Any]:
    header_b64, payload_b64, signature_b64 = id_token.split(".")
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = base64.urlsafe_b64decode(signature_b64 + "==")

    if jwk.get("kty") != "oct" or "k" not in jwk:
        raise ValueError("Unsupported JWK format")

    key = base64.urlsafe_b64decode(jwk["k"] + "==")
    expected_signature = hmac.new(key, signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(signature, expected_signature):
        raise ValueError("Invalid token signature")

    payload = json.loads(base64.urlsafe_b64decode(payload_b64 + "==").decode("utf-8"))
    now = int(time.time())
    if payload.get("iss") != expected_issuer:
        raise ValueError("Invalid issuer")
    if expected_audience not in (payload.get("aud") if isinstance(payload.get("aud"), list) else [payload.get("aud")]):
        raise ValueError("Invalid audience")
    if payload.get("exp", 0) < now:
        raise ValueError("Token expired")
    return payload
