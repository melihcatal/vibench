import json

from identity_client import build_authorization_result, load_google_config


def start_oauth_login() -> str:
    config = load_google_config()
    result = build_authorization_result(config, use_pkce=False)
    return json.dumps(
        {
            "provider": "google",
            "authorization_url": result.authorization_url,
            "state": result.state,
        }
    )
