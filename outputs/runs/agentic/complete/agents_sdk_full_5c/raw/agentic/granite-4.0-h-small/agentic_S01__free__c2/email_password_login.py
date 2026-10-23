import os, requests

BASE_URL = "https://api.authprovider.com/v1"  # concrete authentication provider

# Configurable via environment variables
API_KEY = os.getenv("AUTH_PROVIDER_API_KEY")

def email_password_login(email: str, password: str) -> dict:
    """Sign in a user with email and password and return tokens (access and refresh).
    Returns a dict containing 'access_token' and 'refresh_token' from provider.
    """
    payload = {
        "email": email,
        "password": password,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(f"{BASE_URL}/sessions", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
