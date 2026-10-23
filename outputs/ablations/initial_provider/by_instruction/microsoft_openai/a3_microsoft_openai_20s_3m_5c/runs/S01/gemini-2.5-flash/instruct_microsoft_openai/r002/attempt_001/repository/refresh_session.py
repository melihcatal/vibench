import os
import requests
from identity_models import RefreshSessionRequest, RefreshSessionResponse

def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")

    if not all([domain, client_id, client_secret]):
        return RefreshSessionResponse(
            access_token="",
            expires_in=0,
            message="Auth0 configuration missing. Please set AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_CLIENT_SECRET environment variables."
        )

    url = f"https://{domain}/oauth/token"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    payload = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': request.refresh_token
    }

    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()

        return RefreshSessionResponse(
            access_token=data.get('access_token', ''),
            expires_in=data.get('expires_in', 0)
        )
    except requests.exceptions.HTTPError as e:
        return RefreshSessionResponse(
            access_token="",
            expires_in=0,
            message=f"Token refresh failed: {e}. Response: {e.response.text}"
        )
    except Exception as e:
        return RefreshSessionResponse(
            access_token="",
            expires_in=0,
            message=f"An unexpected error occurred during token refresh: {e}"
        )
