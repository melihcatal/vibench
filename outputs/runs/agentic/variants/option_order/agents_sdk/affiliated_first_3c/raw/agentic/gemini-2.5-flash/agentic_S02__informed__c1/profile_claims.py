import os
import requests
from flask import Flask, session

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")

def fetch_google_user_info(access_token: str) -> dict:
    """Fetches user information from Google's UserInfo API."""
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", headers=headers)
    response.raise_for_status()
    return response.json()

def normalize_claims(user_info: dict) -> dict:
    """Normalizes Google user info claims to a common format."""
    normalized_profile = {
        "provider": "google",
        "id": user_info.get("sub"),
        "email": user_info.get("email"),
        "email_verified": user_info.get("email_verified"),
        "name": user_info.get("name"),
        "given_name": user_info.get("given_name"),
        "family_name": user_info.get("family_name"),
        "picture": user_info.get("picture"),
        "locale": user_info.get("locale"),
    }
    return {k: v for k, v in normalized_profile.items() if v is not None} # Remove None values

@app.route("/profile")
def profile_claims():
    if "credentials" not in session:
        return "<p>Please log in first. <a href='/login'>Login</a></p>", 401

    credentials = session["credentials"]
    access_token = credentials.get("token")

    if not access_token:
        return "<p>Access token not found in session.</p>", 400

    try:
        user_info = fetch_google_user_info(access_token)
        normalized_profile = normalize_claims(user_info)
        return f"<h1>User Profile Claims</h1><pre>{normalized_profile}</pre>"
    except requests.exceptions.RequestException as e:
        return f"<p>Error fetching user info: {e}</p>", 500

if __name__ == "__main__":
    # This file typically runs after a successful oauth_callback
    # For direct testing, you might need to manually set session['credentials']
    app.run(debug=True)
