from typing import Optional

from identity_client import IdentityProviderConfig, exchange_authorization_code
from identity_models import CallbackRequest, OAuthTokenResponse, normalize_claims


def oauth_callback(request: CallbackRequest, config: Optional[IdentityProviderConfig] = None) -> OAuthTokenResponse:
    cfg = config or IdentityProviderConfig.from_env()
    token_payload = exchange_authorization_code(
        cfg=cfg,
        code=request.code,
        redirect_uri=request.redirect_uri or cfg.redirect_uri,
        code_verifier=request.code_verifier,
    )
    claims = normalize_claims(token_payload.claims or {})
    return OAuthTokenResponse(
        access_token=token_payload.access_token,
        id_token=token_payload.id_token,
        refresh_token=token_payload.refresh_token,
        token_type=token_payload.token_type,
        expires_in=token_payload.expires_in,
        scope=token_payload.scope,
        claims=claims,
        provider=cfg.provider_name,
    )
