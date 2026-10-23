from __future__ import annotations

import os
import urllib.parse
from dataclasses import dataclass
from typing import Dict, Optional

from identity_models import AuthRequest, CallbackRequest


@dataclass(frozen=True)
class ProviderConfig:
    provider_name: str
    client_id: Optional[str]
    redirect_uri: Optional[str]
    authorization_endpoint: Optional[str]
    token_endpoint: Optional[str]
    userinfo_endpoint: Optional[str]


def get_provider_config() -> ProviderConfig:
    provider_name = os.environ.get("IDENTITY_PROVIDER", "auth0")
    return ProviderConfig(
        provider_name=provider_name,
        client_id=os.environ.get("OIDC_CLIENT_ID") or os.environ.get(f"{provider_name.upper()}_CLIENT_ID"),
        redirect_uri=os.environ.get("OIDC_REDIRECT_URI"),
        authorization_endpoint=os.environ.get("OIDC_AUTHORIZATION_ENDPOINT"),
        token_endpoint=os.environ.get("OIDC_TOKEN_ENDPOINT"),
        userinfo_endpoint=os.environ.get("OIDC_USERINFO_ENDPOINT"),
    )


def build_authorization_url(endpoint: str, request: AuthRequest) -> str:
    query = {
        "client_id": request.client_id,
        "redirect_uri": request.redirect_uri,
        "response_type": "code",
        "scope": request.scope,
        "state": request.state,
        "nonce": request.nonce,
        "code_challenge": request.code_challenge,
        "code_challenge_method": request.code_challenge_method,
    }
    return f"{endpoint}?{urllib.parse.urlencode(query)}"


def build_token_request_payload(request: CallbackRequest) -> Dict[str, str]:
    payload = {
        "grant_type": "authorization_code",
        "code": request.code,
        "redirect_uri": request.redirect_uri,
        "client_id": request.client_id,
    }
    if request.code_verifier:
        payload["code_verifier"] = request.code_verifier
    return payload
