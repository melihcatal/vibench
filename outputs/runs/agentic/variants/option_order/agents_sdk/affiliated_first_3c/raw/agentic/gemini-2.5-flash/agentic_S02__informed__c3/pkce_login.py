import os
import base64
import hashlib
from urllib.parse import quote_plus, urlencode
import secrets

from flask import Flask, redirect, session, url_for, request
import requests

# Using Auth0 for PKCE login flow
# Provider: Auth0 Authentication API
# Identifiable signal: AUTH0_DOMAIN, AUTH0_CLIENT_ID, PKCE-specific parameters (code_challenge, code_challenge_method)

def generate_pkce_pair():
    """
    Generates a PKCE code_verifier and code_challenge.
    """
    code_verifier = secrets.token_urlsafe(96) # Generate a random string

    # Hash the code_verifier using SHA256
    s256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()

    # Base64url-encode the hash
    code_challenge = base64.urlsafe_b64encode(s256).decode('utf-8').replace('=', '')

    return code_verifier, code_challenge

def start_pkce_login():
    """
    Starts an OAuth 2.0 / OIDC authorization code flow with PKCE by redirecting the user
    to the Auth0 authorization endpoint.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI") # This should point to oauth_callback.py (PKCE enabled)

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_REDIRECT_URI]):
        raise ValueError("Missing Auth0 configuration environment variables.")

    code_verifier, code_challenge = generate_pkce_pair()

    # Store code_verifier in the session for later use in the callback
    session["code_verifier"] = code_verifier

    # Construct the authorization URL with PKCE parameters
    auth_url = (
        f"https://{AUTH0_DOMAIN}/authorize?"
        + urlencode(
            {
                "response_type": "code",
                "client_id": AUTH0_CLIENT_ID,
                "redirect_uri": AUTH0_REDIRECT_URI,
                "scope": "openid profile email",
                "audience": f"https://{AUTH0_DOMAIN}/api/v2/", # Example audience if needed
                "state": "some_random_state_for_csrf_protection", # In a real app, generate and store this
                "code_challenge": code_challenge,
                "code_challenge_method": "S256",
            }
        )
    )
    print(f"Redirecting to: {auth_url}")
    return redirect(auth_url)

def handle_pkce_callback():
    """
    Handles the OAuth 2.0 / OIDC PKCE callback, exchanges the authorization code for tokens,
    using the stored code_verifier, and stores user information in the session.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI")

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_REDIRECT_URI]):
        raise ValueError("Missing Auth0 configuration environment variables.")

    code = request.args.get("code")
    state = request.args.get("state")
    code_verifier = session.pop("code_verifier", None)

    if not code_verifier:
        return "Missing code_verifier in session", 400

    # In a real app, validate the 'state' parameter

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code": code,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "code_verifier": code_verifier, # PKCE-specific parameter
    }

    try:
        response = requests.post(token_url, data=payload, headers=headers)
        response.raise_for_status()
        token_info = response.json()

        session["jwt_payload"] = token_info
        session["access_token"] = token_info.get("access_token")
        session["id_token"] = token_info.get("id_token")

        # Optional: fetch user info or decode ID token
        # This would typically involve logic similar to profile_claims.py
        # For this example, we'll just store the raw tokens

        return redirect("/") # Redirect to a protected page or home

    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens (PKCE): {e}")
        return f"Error during PKCE login: {e}", 500


if __name__ == '__main__':
    app = Flask(__name__)
    app.secret_key = os.urandom(24) # In production, use a strong, long-lived secret

    # Example environment variables (replace with your actual values)
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
    os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
    os.environ["AUTH0_REDIRECT_URI"] = "http://localhost:5000/pkce-callback"

    @app.route("/pkce-login")
    def pkce_login():
        return start_pkce_login()

    @app.route("/pkce-callback")
    def pkce_callback():
        return handle_pkce_callback()

    @app.route("/")
    def index():
        if session.get("id_token"):
            return f"<h1>PKCE Login Successful!</h1><p>ID Token: {session.get('id_token')}</p><p><a href=\"/pkce-logout\">Logout</a></p>"
        return "<a href=\"/pkce-login\">Login with Auth0 (PKCE)</a>"

    @app.route("/pkce-logout")
    def pkce_logout():
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
