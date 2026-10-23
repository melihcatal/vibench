from identity_client import build_authorization_url, create_pkce_pair, load_identity_config


def start_pkce_login() -> tuple[str, str]:
    config = load_identity_config()
    auth = create_pkce_pair()
    return build_authorization_url(config, auth), auth.code_verifier or ""
