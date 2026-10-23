from identity_client import exchange_google_code, load_identity_config


def oauth_callback(code: str) -> dict:
    config = load_identity_config()
    tokens = exchange_google_code(code, config["google_client_id"], config["google_client_secret"], config["google_redirect_uri"])
    return tokens.__dict__
