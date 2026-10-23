import os, requests

BASE_URL = "https://api.authprovider.com/v1"  # concrete authentication provider

# Configurable via environment variables
API_KEY = os.getenv("AUTH_PROVIDER_API_KEY")

def refresh_session(refresh_token: str) -> dict:
    """Refresh an expired access token using the provider's refresh endpoint.
    Returns a dict with a new 'access_token'.
    """
    payload = {
        "refresh_token": refresh_token,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(f"{BASE_URL}/sessions/refresh", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
