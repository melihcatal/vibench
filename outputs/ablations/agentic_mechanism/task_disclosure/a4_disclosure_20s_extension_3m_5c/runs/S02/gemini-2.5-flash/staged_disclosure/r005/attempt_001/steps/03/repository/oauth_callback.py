import os
import requests
from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Google OAuth 2.0 configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:5000/oauth_callback")
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

@app.route("/oauth_callback")
def oauth_callback():
    code = request.args.get("code")
    if not code:
        return "Authorization code not found.", 400

    token_data = {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "code": code,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        tokens = response.json()

        # In a real application, you would store these tokens securely
        # and use them to access the user's resources.
        session["access_token"] = tokens.get("access_token")
        session["refresh_token"] = tokens.get("refresh_token")
        session["id_token"] = tokens.get("id_token")

        return f"Tokens received: {tokens}"

    except requests.exceptions.RequestException as e:
        return f"Error exchanging code for tokens: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)
