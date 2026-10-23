import requests
from identity_client import IdentityClient
from identity_models import RefreshSessionRequest, RefreshSessionResponse

def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    client = IdentityClient()

    if not client.auth0_oauth_base_url:
        raise ValueError("Auth0 client not configured.")

    url = f"{client.auth0_oauth_base_url}/oauth/token"
    headers = {"content-type": "application/json"}
    payload = {
        "grant_type": "refresh_token",
        "client_id": client.auth0_client_id,
        "client_secret": client.auth0_client_secret,
        "refresh_token": request.refresh_token,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        return RefreshSessionResponse(
            access_token=data.get("access_token"),
            expires_in=data.get("expires_in"),
            token_type=data.get("token_type")
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Auth0 session refresh failed: {e}")
