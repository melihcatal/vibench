
import os
import urllib.parse

def start_oauth_login_flow():
    """
    Starts an OAuth or OIDC authorization-code login flow using Auth0.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI") # e.g., "http://localhost:3000/callback"
    AUTH0_SCOPE = os.environ.get("AUTH0_SCOPE", "openid profile email")
    AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE") # Optional, for API authorization

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_REDIRECT_URI]):
        raise ValueError("AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_REDIRECT_URI must be set as environment variables.")

    # Construct the authorization URL
    auth_url_params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "scope": AUTH0_SCOPE,
        "audience": AUTH0_AUDIENCE,
        # "state": "some_random_state_value" # For CSRF protection, should be generated and stored per request
        # "code_challenge": "some_code_challenge", # For PKCE, if pkce_login.py is used
        # "code_challenge_method": "S256" # For PKCE
    }

    # Remove None values from parameters
    auth_url_params = {k: v for k, v in auth_url_params.items() if v is not None}

    query_string = urllib.parse.urlencode(auth_url_params)
    authorization_url = f"https://{AUTH0_DOMAIN}/authorize?{query_string}"

    print(f"Redirecting to: {authorization_url}")
    return authorization_url

if __name__ == "__main__":
    # Example usage:
    # Set environment variables for testing
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
    os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
    os.environ["AUTH0_REDIRECT_URI"] = "http://localhost:3000/callback"

    try:
        url = start_oauth_login_flow()
        print(f"Auth0 Authorization URL: {url}")
    except ValueError as e:
        print(f"Error: {e}")
