import os
import requests
from identity_models import RefreshTokenRequest, RefreshTokenResponse


def refresh_session(request: RefreshTokenRequest) -> RefreshTokenResponse:
    url = f"https://{os.environ.get('AUTH0_DOMAIN')}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": request.grant_type,
        "client_id": request.client_id,
        "client_secret": request.client_secret,
        "refresh_token": request.refresh_token,
    }
    response = requests.post(url, headers=headers, data=payload)
    response.raise_for_status()
    return RefreshTokenResponse(**response.json())
