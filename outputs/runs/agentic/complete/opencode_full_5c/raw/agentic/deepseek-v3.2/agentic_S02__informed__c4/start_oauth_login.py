import os
import secrets
import urllib.parse
from authlib.integrations.requests_client import OAuth2Session


def start_auth0_oauth_login():
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    redirect_uri = os.environ.get(
        "AUTH0_REDIRECT_URI", "http://localhost:3000/callback"
    )

    if not domain or not client_id:
        raise ValueError(
            "Missing AUTH0_DOMAIN or AUTH0_CLIENT_ID environment variables"
        )

    authorization_base_url = f"https://{domain}/authorize"

    session = OAuth2Session(
        client_id, redirect_uri=redirect_uri, scope="openid profile email"
    )

    state = secrets.token_urlsafe(16)

    authorization_url, _ = session.create_authorization_url(
        authorization_base_url, state=state
    )

    return {
        "authorization_url": authorization_url,
        "state": state,
        "provider": "auth0",
        "client_id": client_id,
    }


if __name__ == "__main__":
    result = start_auth0_oauth_login()
    print(f"Redirect user to: {result['authorization_url']}")
    print(f"State parameter: {result['state']}")
