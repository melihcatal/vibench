import os
import boto3
from urllib.parse import urlencode, urljoin

# Amazon Cognito Federation
COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
REDIRECT_URI = "https://your-app.com/oauth_callback"


def start_oauth_login(state=None):
    """Redirect the user to the Cognito hosted login page with an authorization code flow.

    Generates the OAuth URI and returns it so the caller can perform the HTTP redirect.
    """
    # Build parameters
    params = {
        "response_type": "code",
        "client_id": COGNITO_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
        "state": state or "default_state",
    }
    # Construct the authorize URL
    authorize_url = urljoin(COGNITO_DOMAIN, "/oauth2/authorize")
    redirect_uri = f"{authorize_url}?{urlencode(params)}"
    return redirect_uri


if __name__ == "__main__":
    # Example usage -- in a real app this would be a Flask/Django redirect
    url = start_oauth_login()
    print("Redirect the user to this URL to start login:", url)
