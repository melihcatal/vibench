import os
import base64
import hashlib
import secrets
from flask import Flask, redirect, url_for, session, request
import requests

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecret")

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
REDIRECT_URI = "http://localhost:5000/pkce_callback"
SCOPES = ["openid", "email", "profile"]

def generate_pkce_codes():
    code_verifier = secrets.token_urlsafe(96)  # Generate a random string
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8").replace("=", "")
    return code_verifier, code_challenge

def start_google_pkce_login():
    code_verifier, code_challenge = generate_pkce_codes()
    session["code_verifier"] = code_verifier

    authorization_url = (
        f"{GOOGLE_AUTH_URI}?"
        f"response_type=code&"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope={' '.join(SCOPES)}&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method=S256"
    )
    return redirect(authorization_url)

def handle_google_pkce_callback():
    code = request.args.get("code")
    if not code:
        return "Error: No authorization code received."

    code_verifier = session.pop("code_verifier", None)
    if not code_verifier:
        return "Error: Code verifier not found in session."

    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(GOOGLE_TOKEN_URI, data=token_data)
        response.raise_for_status()
        tokens = response.json()
        session["pkce_tokens"] = tokens
        return "PKCE Login Successful! Tokens stored in session."
    except requests.exceptions.RequestException as e:
        return f"Error exchanging code for tokens: {e}"

if __name__ == "__main__":
    # This is a minimal example and not a production-ready server.
    # For demonstration purposes, you would integrate this into your Flask app routes.
    with app.test_request_context():
        # Simulate starting the login flow and then handling a callback
        print("Simulating PKCE login start...")
        # The actual redirect would happen here
        # For testing, you'd manually visit the authorization_url and then come back to /pkce_callback

        # Simulate handling the callback
        # You would replace 'mock_code' with a real authorization code obtained from Google
        mock_auth_code = "mock_authorization_code_from_google"
        session["code_verifier"], _ = generate_pkce_codes() # Generate a verifier for the mock callback
        with app.test_request_context(f'/pkce_callback?code={mock_auth_code}'):
            print("Simulating PKCE callback handling...")
            # In a real scenario, this would involve a POST request to Google token endpoint.
            # For this isolated file execution, we'll just show the function call.
            # print(handle_google_pkce_callback())
            print("PKCE callback logic would be executed here.")

