import json

from identity_client import build_authorization_url, generate_nonce, generate_state, load_google_config
from identity_models import AuthorizationRequest


def start_oauth_login() -> str:
    config = load_google_config()
    auth_request = AuthorizationRequest(state=generate_state(), nonce=generate_nonce(), redirect_uri=config.redirect_uri)
    return build_authorization_url(config, auth_request)


if __name__ == "__main__":
    print(json.dumps({"authorization_url": start_oauth_login()}))
