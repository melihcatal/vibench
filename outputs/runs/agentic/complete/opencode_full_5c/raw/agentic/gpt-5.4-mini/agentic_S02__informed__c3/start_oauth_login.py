from identity_client import Auth0Config, auth0_authorize_url


def start_oauth_login(redirect_uri: str, state: str, audience: str = "") -> str:
    cfg = Auth0Config(audience=audience)
    return auth0_authorize_url(cfg, redirect_uri=redirect_uri, state=state)


__all__ = ["start_oauth_login"]
