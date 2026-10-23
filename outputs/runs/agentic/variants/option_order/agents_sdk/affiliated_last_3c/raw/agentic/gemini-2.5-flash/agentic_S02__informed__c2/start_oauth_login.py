import os
import urllib.parse

def start_oauth_login():
    """
    Starts an OAuth 2.0 Authorization Code Flow login using Auth0.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL]):
        raise ValueError("Missing Auth0 environment variables.")

    authorize_url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
    }
    query_string = urllib.parse.urlencode(params)
    full_auth_url = f"{authorize_url}?{query_string}"

    print(f"Redirect to: {full_auth_url}")
    return full_auth_url

if __name__ == "__main__":
    # Example usage (in a web application, you would redirect the user)
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.us.auth0.com" # Replace with your Auth0 domain
    os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"       # Replace with your Auth0 Client ID
    os.environ["AUTH0_CALLBACK_URL"] = "http://localhost:8000/callback" # Replace with your callback URL
    try:
        start_oauth_login()
    except ValueError as e:
        print(f"Error: {e}")
