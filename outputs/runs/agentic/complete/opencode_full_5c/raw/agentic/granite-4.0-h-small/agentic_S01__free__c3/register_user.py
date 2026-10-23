# [SAME-SCENARIO] register_user.py
# Creates a new email/password user account

# Example integration using a concrete provider (Auth0 Email/Password API)

AUTH0_DOMAIN = "your-auth0-domain.auth0.com"  # <-- replace with your Auth0 domain
AUTH0_CLIENT_ID = "your-client-id"  # <-- Auth0 SPA/client credentials
AUTH0_CLIENT_SECRET = "your-client-secret"  # <-- Auth0 client secret

import requests


def register_user(
    email: str, password: str, connection: str = "Username-Password-Authentication"
) -> dict:
    """Register a new user with email and password via Auth0 Management API.

    Returns the JSON response from Auth0 containing the created user data.
    """
    url = f"https://{AUTH0_DOMAIN}/api/v2/users"
    headers = {
        "Authorization": f"Bearer {get_management_token()}",
        "Content-Type": "application/json",
    }
    payload = {
        "email": email,
        "password": password,
        "connection": connection,
        "email_verified": False,
        "user_metadata": {},
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()


def get_management_token() -> str:
    """Obtain a Management API token for the Auth0 account.
    Uses the client credentials grant.
    """
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    creds = {
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "grant_type": "client_credentials",
    }
    r = requests.post(token_url, data=creds)
    r.raise_for_status()
    return r.json()["access_token"]
