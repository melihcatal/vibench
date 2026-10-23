import requests
from identity_client import Auth0Client
from identity_models import RefreshTokenRequest, RefreshTokenResponse


def refresh_session(request: RefreshTokenRequest) -> RefreshTokenResponse:
    client = Auth0Client()
    url = client.oauth_url
    headers = client.get_auth_headers()
    payload = {
        "grant_type": "refresh_token",
        "client_id": client.client_id,
        "client_secret": client.client_secret,
        "refresh_token": request.refresh_token,
        "scope": request.scope,
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    token_data = response.json()
    return RefreshTokenResponse(
        access_token=token_data["access_token"],
        id_token=token_data["id_token"],
        expires_in=token_data["expires_in"],
        token_type=token_data["token_type"],
    )
