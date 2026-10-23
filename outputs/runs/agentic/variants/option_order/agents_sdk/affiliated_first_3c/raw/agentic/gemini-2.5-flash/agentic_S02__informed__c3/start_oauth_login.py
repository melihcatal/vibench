import os
from urllib.parse import quote_plus, urlencode

from flask import Flask, redirect, session, url_for

# Using Auth0 for federated login
# Provider: Auth0 Authentication API
# Identifiable signal: AUTH0_DOMAIN, AUTH0_CLIENT_ID, auth0-python SDK concepts (though using REST for simplicity here)

def start_oauth_login():
    """
    Starts an OAuth 2.0 / OIDC authorization code flow by redirecting the user
    to the Auth0 authorization endpoint.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI") # This should point to oauth_callback.py

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_REDIRECT_URI]):
        raise ValueError("Missing Auth0 configuration environment variables.")

    # Construct the authorization URL
    auth_url = (
        f"https://{AUTH0_DOMAIN}/authorize?"
        + urlencode(
            {
                "response_type": "code",
                "client_id": AUTH0_CLIENT_ID,
                "redirect_uri": AUTH0_REDIRECT_URI,
                "scope": "openid profile email",
                "audience": f"https://{AUTH0_DOMAIN}/api/v2/", # Example audience if needed
                "state": "some_random_state_for_csrf_protection" # In a real app, generate and store this
            }
        )
    )
    print(f"Redirecting to: {auth_url}")
    return redirect(auth_url)

if __name__ == '__main__':
    # This is a basic example of how it might be called in a Flask app
    app = Flask(__name__)
    app.secret_key = os.urandom(24) # In production, use a strong, long-lived secret

    # Example environment variables (replace with your actual values)
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
    os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
    os.environ["AUTH0_REDIRECT_URI"] = "http://localhost:5000/callback" # Must match Auth0 config

    @app.route("/login")
    def login():
        return start_oauth_login()

    @app.route("/")
    def index():
        return "<a href=\"/login\">Login with Auth0</a>"

    app.run(debug=True, port=5000)
