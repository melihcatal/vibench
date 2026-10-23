import os
import requests
from identity_models import RefreshSessionRequest, RefreshSessionResponse

def refresh_session(refresh_token: str) -> RefreshSessionResponse:
    domain = os.getenv("AUTH0_DOMAIN")
    client_id = os.getenv("AUTH0_CLIENT_ID")
    client_secret = os.getenv("AUTH0_CLIENT_SECRET")
    
    token_url = f"https://{domain}/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }
    
    response = requests.post(token_url, json=payload)
    response.raise_for_status()
    token_data = response.json()
    
    return RefreshSessionResponse(
        access_token=token_data["access_token"],
        id_token=token_data.get("id_token"),
        expires_in=token_data["expires_in"]
    )