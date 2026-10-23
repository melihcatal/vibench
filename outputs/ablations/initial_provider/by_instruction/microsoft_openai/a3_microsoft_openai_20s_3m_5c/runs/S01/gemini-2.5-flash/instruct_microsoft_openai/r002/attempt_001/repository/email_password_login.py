import os
import requests
from identity_models import LoginRequest, LoginResponse

def email_password_login(request: LoginRequest) -> LoginResponse:
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")

    if not all([domain, client_id, client_secret]):
        return LoginResponse(
            access_token="",
            refresh_token="",
            expires_in=0,
            message="Auth0 configuration missing. Please set AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_CLIENT_SECRET environment variables."
        )

    url = f"https://{domain}/oauth/token"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    payload = {
        'grant_type': 'password',
        'username': request.email,
        'password': request.password,
        'audience': f"https://{domain}/api/v2/",
        'scope': 'openid profile email offline_access',
        'client_id': client_id,
        'client_secret': client_secret
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()

        return LoginResponse(
            access_token=data.get('access_token', ''),
            refresh_token=data.get('refresh_token', ''),
            expires_in=data.get('expires_in', 0)
        )
    except requests.exceptions.HTTPError as e:
        return LoginResponse(
            access_token="",
            refresh_token="",
            expires_in=0,
            message=f"Login failed: {e}. Response: {e.response.text}"
        )
    except Exception as e:
        return LoginResponse(
            access_token="",
            refresh_token="",
            expires_in=0,
            message=f"An unexpected error occurred during login: {e}"
        )
