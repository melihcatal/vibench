from __future__ import annotations

from identity_client import build_auth0_authorization_url, generate_pkce_pair, generate_state, load_auth0_config



def start_pkce_login(redirect_uri: str | None = None, scope: str = "openid profile email") -> dict:
    config = load_auth0_config()
    effective_redirect_uri = redirect_uri or config.default_redirect_uri
    if not effective_redirect_uri:
        raise ValueError("redirect_uri is required for Auth0 PKCE flow")
    pkce = generate_pkce_pair()
    state = generate_state()
    authorization_url = build_auth0_authorization_url(
        redirect_uri=effective_redirect_uri,
        state=state,
        scope=scope,
        code_challenge=pkce["code_challenge"],
        code_challenge_method=pkce["code_challenge_method"],
    )
    return {
        "provider": "Auth0 Authentication API",
        "authorization_url": authorization_url,
        "state": state,
        "code_verifier": pkce["code_verifier"],
        "code_challenge": pkce["code_challenge"],
        "code_challenge_method": pkce["code_challenge_method"],
        "redirect_uri": effective_redirect_uri,
    }
