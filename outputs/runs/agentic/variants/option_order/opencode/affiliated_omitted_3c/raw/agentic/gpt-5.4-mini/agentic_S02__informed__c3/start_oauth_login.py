import secrets

from identity_client import build_client


def start_oauth_login() -> dict[str, str]:
    client = build_client()
    state = secrets.token_urlsafe(32)
    url = client.authorization_url('code', 'openid profile email', state)
    return {'authorization_url': url, 'state': state}
