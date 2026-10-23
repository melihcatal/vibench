import json

from identity_client import build_authorization_result, load_google_config


def start_pkce_login() -> str:
    config = load_google_config()
    result = build_authorization_result(config, use_pkce=True)
    return json.dumps(
        {
            "provider": "google",
            "authorization_url": result.authorization_url,
            "state": result.state,
            "code_verifier": result.code_verifier,
            "code_challenge": result.code_challenge,
        }
    )
