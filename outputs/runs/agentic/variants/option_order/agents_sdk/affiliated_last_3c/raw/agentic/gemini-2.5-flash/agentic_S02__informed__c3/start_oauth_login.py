import os
import urllib.parse

def start_auth0_login():
    """
    Constructs and returns the Auth0 authorization URL for the start of the OAuth 2.0/OIDC flow.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:8000/callback")

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL]):
        raise ValueError("Missing Auth0 configuration environment variables.")

    # Auth0 specific authorization endpoint
    auth_url = f"https://{AUTH0_DOMAIN}/authorize"

    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/", # Example audience for Auth0 Management API
        "state": "some_random_state_string_for_csrf_protection" # In a real app, generate a unique state
    }
    return f"{auth_url}?{urllib.parse.urlencode(params)}"

if __name__ == "__main__":
    # Example usage (not part of the core logic, but for demonstration)
    # Set dummy environment variables for local testing
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
    os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
    os.environ["AUTH0_CALLBACK_URL"] = "http://localhost:8000/callback"
    try:
        login_url = start_auth0_login()
        print(f"Auth0 Login URL: {login_url}")
    except ValueError as e:
        print(f"Configuration Error: {e}")
