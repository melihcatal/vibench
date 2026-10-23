from typing import Optional

from identity_client import IdentityProviderConfig, build_authorization_url
from identity_models import PKCELoginRequest, PKCELoginStartResponse, create_pkce_pair


def pkce_login(request: PKCELoginRequest, config: Optional[IdentityProviderConfig] = None) -> PKCELoginStartResponse:
    cfg = config or IdentityProviderConfig.from_env()
    code_verifier, code_challenge = create_pkce_pair()
    auth_url = build_authorization_url(
        cfg=cfg,
        redirect_uri=request.redirect_uri,
        state=request.state,
        code_challenge=code_challenge,
        scope=request.scope,
        nonce=request.nonce,
        response_mode=request.response_mode,
    )
    return PKCELoginStartResponse(
        authorization_url=auth_url,
        code_verifier=code_verifier,
        code_challenge=code_challenge,
        state=request.state,
        provider=cfg.provider_name,
        client_id=cfg.client_id,
    )
