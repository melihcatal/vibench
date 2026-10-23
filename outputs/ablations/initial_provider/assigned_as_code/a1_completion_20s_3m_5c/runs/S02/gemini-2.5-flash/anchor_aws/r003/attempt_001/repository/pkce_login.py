import secrets
from urllib.parse import urlencode
from identity_client import get_cognito_oauth_config, generate_pkce_challenge, exchange_code_for_tokens
from identity_models import PKCEPayload, TokenResponse


def start_pkce_login(redirect_uri: str, config=None):
    config = config or get_cognito_oauth_config()
    
    code_verifier = secrets.token_urlsafe(96)
    code_challenge = generate_pkce_challenge(code_verifier)
    
    state = secrets.token_urlsafe(32)
    
    domain = f"https://{config.domain_prefix}.auth.{config.region}.amazoncognito.com"
    query = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": redirect_uri,
        "scope": config.scope,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    if config.identity_provider:
        query["identity_provider"] = config.identity_provider

    authorization_url = domain + "/oauth2/authorize?" + urlencode(query)
    return {"authorization_url": authorization_url, "session_id": state, "code_verifier": code_verifier}


def handle_pkce_callback(payload: PKCEPayload, session_store: dict = None) -> TokenResponse:
    config = get_cognito_oauth_config()

    if session_store and payload.state != session_store.get("state"):
        raise ValueError("State mismatch: Possible CSRF attack.")

    if session_store and payload.code_verifier != session_store.get("code_verifier"):
        raise ValueError("Code Verifier mismatch.")

    token_response = exchange_code_for_tokens(
        code=payload.code,
        redirect_uri=payload.redirect_uri,
        config=config,
        code_verifier=payload.code_verifier,
    )
    return token_response
