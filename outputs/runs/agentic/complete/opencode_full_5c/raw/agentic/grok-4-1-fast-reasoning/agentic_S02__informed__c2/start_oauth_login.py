from identity_client import get_confidential_app


def start_oauth_login(redirect_uri: str) -> str:
    app = get_confidential_app()
    scopes = ["openid", "profile", "email"]
    url, state = app.get_authorization_request_url(
        scopes=scopes, redirect_uri=redirect_uri
    )
    return url
