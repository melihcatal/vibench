import os
import requests
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(refresh_token: str) -> RefreshResponse:
    auth0_domain = os.getenv("AUTH0_DOMAIN")
    client_id = os.getenv("AUTH0_CLIENT_ID")
    token_url = f"https://{auth0_domain}/oauth/token"

    request = RefreshRequest(refresh_token=refresh_token, client_id=client_id)
    payload = {
        "grant_type": request.grant_type,
        "client_id": request.client_id,
        "refresh_token": request.refresh_token,
    }
    response = requests.post(token_url, json=payload)
    response.raise_for_status()
    data = response.json()
    return RefreshResponse(
        access_token=data["access_token"],
        expires_in=data["expires_in"],
        id_token=data.get("id_token", ""),
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        refresh_token = sys.argv[1]
        response = refresh_session(refresh_token)
        print(f"New Access Token: {response.access_token}")
