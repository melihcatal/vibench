import os
import boto3
import requests
from urllib.parse import parse_qs

# Amazon Cognito Federation
COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
COGNITO_CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET")
REDIRECT_URI = "https://your-app.com/oauth_callback"

TOKEN_ENDPOINT = f"{COGNITO_DOMAIN}/oauth2/token"


def exchange_authorization_code(code):
    """Exchange an authorization code for an access token and ID token from Cognito.

    Returns a dict containing 'id_token', 'access_token', 'refresh_token', and 'expires_in'.
    """
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": COGNITO_CLIENT_ID,
        "client_secret": COGNITO_CLIENT_SECRET,
    }
    try:
        response = requests.post(TOKEN_ENDPOINT, data=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to exchange code for tokens: {exc}")


if __name__ == "__main__":
    # Demo: expects 'code' query parameter in the request
    from flask import Flask, request

    app = Flask(__name__)

    @app.route("/oauth_callback")
    def callback():
        code = request.args.get("code")
        if not code:
            return "Missing code parameter", 400
        try:
            tokens = exchange_authorization_code(code)
            return f"Tokens received: {tokens}", 200
        except Exception as e:
            return str(e), 500

    # Run locally for testing
    app.run(debug=True)
