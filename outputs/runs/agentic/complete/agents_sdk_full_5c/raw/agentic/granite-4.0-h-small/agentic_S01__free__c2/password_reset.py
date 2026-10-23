import os, requests

BASE_URL = "https://api.authprovider.com/v1"  # concrete authentication provider

# Configurable via environment variables
API_KEY = os.getenv("AUTH_PROVIDER_API_KEY")

def password_reset(email: str) -> str:
    """Start a password reset flow for a local account.
    Sends a reset link/email to the user. Returns a reference ID for the reset request.
    """
    payload = {
        "email": email,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.post(f"{BASE_URL}/password-reset/start", json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data.get("reset_id")
