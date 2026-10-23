import os, requests

BASE_URL = "https://api.authprovider.com/v1"  # concrete authentication provider

# Configurable via environment variables
API_KEY = os.getenv("AUTH_PROVIDER_API_KEY")

def register_user(email: str, password: str, locale: str = "en") -> dict:
    """Create a new email/password user account using the provider's API.
    Returns the JSON response from the provider containing user ID, session token, etc.
    """
    payload = {
        "email": email,
        "password": password,
        "locale": locale,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(f"{BASE_URL}/users/register", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
