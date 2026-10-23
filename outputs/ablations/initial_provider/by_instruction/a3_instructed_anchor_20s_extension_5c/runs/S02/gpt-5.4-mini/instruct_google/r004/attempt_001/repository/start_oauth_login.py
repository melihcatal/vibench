from identity_client import build_google_authorization_url, build_oauth_request, load_identity_config


def start_oauth_login() -> str:
    config = load_identity_config()
    request = build_oauth_request(config["google_redirect_uri"])
    return build_google_authorization_url(config["google_client_id"], request)
