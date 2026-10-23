# [SAME-SCENARIO] password_reset.py
# Starts a password reset flow for a local account

# Example using Auth0's password reset endpoint (concrete provider)

AUTH0_DOMAIN = "your-auth0-domain.auth0.com"  # <-- replace with your Auth0 domain

import requests


def start_password_reset(
    email: str, connection: str = "Username-Password-Authentication"
) -> dict:
    """Initiates a password reset for the given email.
    Sends a POST to Auth0's /dbconnections/change_password endpoint.
    Returns the HTTP response JSON (usually empty with status 204).
    """
    url = f"https://{AUTH0_DOMAIN}/dbconnections/change_password"
    payload = {"email": email, "connection": connection, "client_id": AUTH0_CLIENT_ID}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
