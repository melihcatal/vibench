from identity_client import (
    AUTH0_CLIENT_ID,
    AUTH0_REDIRECT_URI,
    AUTH0_DOMAIN,
    authorization_url,
    create_authorization_request,
    load_config,
)


def start_oauth_login() -> str:
    config = load_config()
    request = create_authorization_request(redirect_uri=AUTH0_REDIRECT_URI)
    return authorization_url(config, request)


if __name__ == "__main__":
    print(start_oauth_login())
