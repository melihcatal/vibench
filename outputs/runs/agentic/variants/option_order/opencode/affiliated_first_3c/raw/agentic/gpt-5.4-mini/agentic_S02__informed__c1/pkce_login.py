from identity_client import (
    AUTH0_REDIRECT_URI,
    authorization_url,
    create_authorization_request,
    load_config,
)


def start_pkce_login() -> dict:
    config = load_config()
    request = create_authorization_request(
        redirect_uri=AUTH0_REDIRECT_URI, use_pkce=True
    )
    return {
        "authorization_url": authorization_url(config, request),
        "state": request.state,
        "nonce": request.nonce,
        "code_verifier": request.code_verifier,
    }
