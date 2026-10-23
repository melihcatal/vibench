import os
import json
from urllib.parse import urlencode

import requests
from flask import Flask, redirect, session, url_for, request

# Using Auth0 for federated login callback
# Provider: Auth0 Authentication API
# Identifiable signal: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, requests to Auth0 token endpoint

def handle_oauth_callback():
    """
    Handles the OAuth 2.0 / OIDC callback, exchanges the authorization code for tokens,
    and stores user information in the session.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
    AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI")

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_REDIRECT_URI]):
        raise ValueError("Missing Auth0 configuration environment variables.")

    code = request.args.get("code")
    state = request.args.get("state")

    # In a real app, validate the 'state' parameter against the one sent in start_oauth_login
    # if state != session.get('oauth_state'):
    #     return "State mismatch", 400

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": AUTH0_REDIRECT_URI,
    }

    try:
        response = requests.post(token_url, data=payload, headers=headers)
        response.raise_for_status()
        token_info = response.json()

        session["jwt_payload"] = token_info # Contains id_token, access_token, etc.
        session["access_token"] = token_info.get("access_token")
        session["id_token"] = token_info.get("id_token")

        # Optionally, fetch user profile using the access token
        # This would typically be handled by profile_claims.py
        # For a quick verification, we can include it here
        userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
        userinfo_headers = {
            "Authorization": f"Bearer {token_info.get("access_token")}"
        }
        userinfo_response = requests.get(userinfo_url, headers=userinfo_headers)
        userinfo_response.raise_for_status()
        user_profile = userinfo_response.json()

        session["profile"] = {
            "user_id": user_profile.get("sub"),
            "name": user_profile.get("name"),
            "email": user_profile.get("email"),
            "picture": user_profile.get("picture"),
        }

        return redirect("/") # Redirect to a protected page or home

    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens: {e}")
        return f"Error during login: {e}", 500

if __name__ == '__main__':
    app = Flask(__name__)
    app.secret_key = os.urandom(24) # In production, use a strong, long-lived secret

    # Example environment variables (replace with your actual values)
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
    os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
    os.environ["AUTH0_CLIENT_SECRET"] = "YOUR_AUTH0_CLIENT_SECRET"
    os.environ["AUTH0_REDIRECT_URI"] = "http://localhost:5000/callback"

    @app.route("/callback")
    def callback():
        return handle_oauth_callback()

    @app.route("/")
    def index():
        profile = session.get("profile")
        if profile:
            return f"<h1>Welcome, {profile.get('name')}!</h1><pre>{json.dumps(profile, indent=2)}</pre><p><a href=\"/logout\">Logout</a></p>"
        return "<a href=\"/login\">Login with Auth0</a>"

    @app.route("/login")
    def login():
        from start_oauth_login import start_oauth_login
        return start_oauth_login()

    @app.route("/logout")
    def logout():
        session.clear()
        # Redirect to Auth0 logout endpoint
        logout_url = (
            f"https://{os.environ.get('AUTH0_DOMAIN')}/v2/logout?"
            + urlencode(
                {
                    "returnTo": "http://localhost:5000",
                    "client_id": os.environ.get("AUTH0_CLIENT_ID"),
                },
                quote_via=quote_plus,
            )
        )
        return redirect(logout_url)

    app.run(debug=True, port=5000)
