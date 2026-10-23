import requests
from identity_client import IdentityClient
from identity_models import LoginRequest, LoginResponse

def email_password_login(request: LoginRequest) -> LoginResponse:
    client = IdentityClient()

    if not client.auth0_oauth_base_url:
        raise ValueError("Auth0 client not configured.")

    url = f"{client.auth0_oauth_base_url}/oauth/token"
    headers = {"content-type": "application/json"}
    payload = {
        "grant_type": "password",
        "username": request.email,
        "password": request.password,
        "audience": client.auth0_audience,
        "client_id": client.auth0_client_id,
        "client_secret": client.auth0_client_secret,
        "scope": "openid profile email offline_access"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        return LoginResponse(
            access_token=data.get("access_token"),
            refresh_token=data.get("refresh_token"),
            expires_in=data.get("expires_in"),
            token_type=data.get("token_type")
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Auth0 login failed: {e}")

