import os
from authlib.integrations.requests_client import OAuth2Session


def handle_auth0_callback(authorization_response, expected_state):
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
    redirect_uri = os.environ.get(
        "AUTH0_REDIRECT_URI", "http://localhost:3000/callback"
    )

    if not domain or not client_id or not client_secret:
        raise ValueError("Missing Auth0 environment variables")

    token_url = f"https://{domain}/oauth/token"

    session = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)

    try:
        token = session.fetch_token(
            token_url,
            authorization_response=authorization_response,
            state=expected_state,
        )

        return {
            "access_token": token.get("access_token"),
            "id_token": token.get("id_token"),
            "refresh_token": token.get("refresh_token"),
            "expires_in": token.get("expires_in"),
            "token_type": token.get("token_type"),
            "provider": "auth0",
        }
    except Exception as e:
        raise Exception(f"Failed to exchange code for tokens: {str(e)}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(
            "Usage: python oauth_callback.py <authorization_response_url> <expected_state>"
        )
        sys.exit(1)

    auth_response = sys.argv[1]
    expected_state = sys.argv[2]

    tokens = handle_auth0_callback(auth_response, expected_state)
    print(f"Access token: {tokens['access_token'][:50]}...")
    print(f"ID token: {tokens['id_token'][:50]}...")
