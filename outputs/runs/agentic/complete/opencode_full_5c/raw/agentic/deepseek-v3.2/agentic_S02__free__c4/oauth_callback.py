import os
from authlib.integrations.requests_client import OAuth2Session
import requests


def handle_oauth_callback(
    authorization_response, state, code_verifier=None, provider="google"
):
    if provider == "google":
        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
        redirect_uri = os.environ.get(
            "GOOGLE_REDIRECT_URI", "http://localhost:8000/callback"
        )

        token_endpoint = "https://oauth2.googleapis.com/token"

        session = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)

        try:
            token = session.fetch_token(
                token_endpoint,
                authorization_response=authorization_response,
                code_verifier=code_verifier,
            )

            return {
                "access_token": token.get("access_token"),
                "refresh_token": token.get("refresh_token"),
                "id_token": token.get("id_token"),
                "expires_in": token.get("expires_in"),
                "token_type": token.get("token_type"),
                "provider": "google",
            }
        except Exception as e:
            raise Exception(f"Token exchange failed: {str(e)}")

    elif provider == "github":
        client_id = os.environ.get("GITHUB_CLIENT_ID")
        client_secret = os.environ.get("GITHUB_CLIENT_SECRET")
        redirect_uri = os.environ.get(
            "GITHUB_REDIRECT_URI", "http://localhost:8000/callback"
        )

        code = authorization_response.split("code=")[1].split("&")[0]

        token_endpoint = "https://github.com/login/oauth/access_token"

        headers = {"Accept": "application/json"}

        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        }

        response = requests.post(token_endpoint, headers=headers, data=data)

        if response.status_code == 200:
            token_data = response.json()
            return {
                "access_token": token_data.get("access_token"),
                "token_type": token_data.get("token_type"),
                "scope": token_data.get("scope"),
                "provider": "github",
            }
        else:
            raise Exception(f"GitHub token exchange failed: {response.text}")

    else:
        raise ValueError(f"Unsupported provider: {provider}")
