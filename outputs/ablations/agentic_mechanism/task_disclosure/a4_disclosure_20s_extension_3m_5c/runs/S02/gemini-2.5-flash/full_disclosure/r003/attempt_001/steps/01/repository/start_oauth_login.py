import os
import urllib.parse

def start_oauth_login():
    # Auth0 specific configuration
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_CALLBACK_URL = "http://localhost:3000/callback"  # This should be configured in Auth0
    AUTH0_AUDIENCE = "YOUR_API_AUDIENCE"  # Replace with your API audience if you have one or remove

    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID:
        raise ValueError("AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables must be set.")

    # Standard OAuth 2.0 / OIDC parameters
    response_type = "code"
    scope = "openid profile email"
    # In a real application, generate a secure random state and store it in the session for CSRF protection
    state = "some_random_state_for_now"

    authorize_url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "response_type": response_type,
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": scope,
        "state": state,
        "audience": AUTH0_AUDIENCE # Include if you are calling an API, otherwise can be omitted
    }

    query_string = urllib.parse.urlencode(params)
    full_auth_url = f"{authorize_url}?{query_string}"

    return full_auth_url