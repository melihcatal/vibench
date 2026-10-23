import os
import requests
import time

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_MANAGEMENT_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_MANAGEMENT_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_MANAGEMENT_AUDIENCE = f"https://{{AUTH0_DOMAIN}}/api/v2/"

# Simple in-memory cache for the management API token
_management_api_token = None
_token_expires_at = 0

def get_auth0_management_api_token():
    global _management_api_token, _token_expires_at

    if _management_api_token and time.time() < _token_expires_at:
        return _management_api_token

    url = f"https://{{AUTH0_DOMAIN}}/oauth/token"
    headers = {"Content-Type": "application/json"}
    payload = {
        "client_id": AUTH0_MANAGEMENT_CLIENT_ID,
        "client_secret": AUTH0_MANAGEMENT_CLIENT_SECRET,
        "audience": AUTH0_MANAGEMENT_AUDIENCE,
        "grant_type": "client_credentials"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        token_data = response.json()
        _management_api_token = token_data.get("access_token")
        # Reduce expiry by a few seconds to account for network latency
        _token_expires_at = time.time() + token_data.get("expires_in", 3600) - 60
        return _management_api_token
    except requests.exceptions.RequestException as e:
        print(f"Error getting Auth0 Management API token: {e}")
        if e.response:
            print(f"Response: {e.response.json()}")
        return None
