import base64
import hashlib
import os
import secrets
from typing import Dict, Optional

from identity_client import IdentityProviderConfig, build_authorization_url
from identity_models import LoginRequest, LoginStartResponse, create_pkce_pair


def start_oauth_login(request: LoginRequest, config: Optional[IdentityProviderConfig] = None) -> LoginStartResponse:
    cfg = config or IdentityProviderConfig.from_env()
    if not request.redirect_uri:
        request.redirect_uri = cfg.redirect_uri
    state = request.state or secrets.token_urlsafe(32)
    code_verifier, code_challenge = create_pkce_pair()
    auth_url = build_authorization_url(
        cfg=cfg,
        redirect_uri=request.redirect_uri,
        state=state,
        code_challenge=code_challenge,
        scope=request.scope,
        nonce=request.nonce,
        response_mode=request.response_mode,
    )
    return LoginStartResponse(
        authorization_url=auth_url,
        state=state,
        code_verifier=code_verifier,
        code_challenge=code_challenge,
        provider=cfg.provider_name,
        client_id=cfg.client_id,
    )
