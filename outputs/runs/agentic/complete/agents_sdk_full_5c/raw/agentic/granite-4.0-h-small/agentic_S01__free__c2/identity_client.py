import os

# Configurable via environment variables
BASE_URL = os.getenv("AUTH_PROVIDER_BASE_URL", "https://api.authprovider.com/v1")
API_KEY = os.getenv("AUTH_PROVIDER_API_KEY")

def create_headers() -> dict:
    """Return headers with provider auth credentials."""
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

# Simple thin wrapper around the provider's authentication endpoints

def register_user(email: str, password: str, locale: str = "en") -> dict:
    payload = {"email": email, "password": password, "locale": locale}
    response = requests.post(f"{BASE_URL}/users/register", json=payload, headers=create_headers())
    response.raise_for_status()
    return response.json()


def email_password_login(email: str, password: str) -> dict:
    payload = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/sessions", json=payload, headers=create_headers())
    response.raise_for_status()
    return response.json()


def refresh_session(refresh_token: str) -> dict:
    payload = {"refresh_token": refresh_token}
    response = requests.post(f"{BASE_URL}/sessions/refresh", json=payload, headers=create_headers())
    response.raise_for_status()
    return response.json()


def password_reset(email: str) -> str:
    payload = {"email": email}
    response = requests.post(f"{BASE_URL}/password-reset/start", json=payload, headers=create_headers())
    response.raise_for_status()
    return response.json().get("reset_id")
