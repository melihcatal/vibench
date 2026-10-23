import os
import requests
import json
from identity_client import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI
from identity_models import TokenResponse

def handle_google_oauth_callback(auth_code: str) -> TokenResponse:
    token_url = "https://oauth2.googleapis.com/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "code": auth_code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    token_data = response.json()
    return TokenResponse(
        access_token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token"),
        id_token=token_data.get("id_token"),
        expires_in=token_data.get("expires_in")
    )
