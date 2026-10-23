# SAME-SCENARIO: oauth_callback.py
# Handles OAuth callback and exchanges authorization code for tokens using Auth0

import os
import sys
import requests

# Auth0 configuration (provider identifiable)
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:3000/oauth_callback"


# Exchange code for tokens
def exchange_code_for_tokens(code):
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    return response.json()


# Callback handler (mock)
def oauth_callback():
    # In a real web app, this function would be invoked by the framework at /oauth_callback
    if "code" not in sys.argv:
        print("Error: No authorization code provided")
        return
    code = sys.argv[1]
    try:
        tokens = exchange_code_for_tokens(code)
        print("Tokens received:", tokens)
    except Exception as e:
        print("Token exchange failed:", e)


if __name__ == "__main__":
    oauth_callback()
