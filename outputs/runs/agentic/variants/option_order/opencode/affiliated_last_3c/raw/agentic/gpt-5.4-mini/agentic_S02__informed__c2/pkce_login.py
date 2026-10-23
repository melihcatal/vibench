import json

from identity_client import (
    build_authorization_request,
    discovery_document,
    load_oidc_config,
    token_exchange,
)


def start_pkce_login() -> str:
    config = load_oidc_config()
    oidc = discovery_document(config.issuer)
    auth = build_authorization_request()
    return json.dumps(
        {
            "authorization_url": oidc["authorization_endpoint"],
            "client_id": config.client_id,
            "code_challenge": auth.code_challenge,
            "code_challenge_method": "S256",
            "state": auth.state,
            "nonce": auth.nonce,
            "code_verifier": auth.code_verifier,
        }
    )


def complete_pkce_login(code: str, redirect_uri: str, code_verifier: str) -> str:
    config = load_oidc_config()
    oidc = discovery_document(config.issuer)
    return json.dumps(
        token_exchange(
            oidc["token_endpoint"], config, code, redirect_uri, code_verifier
        )
    )
