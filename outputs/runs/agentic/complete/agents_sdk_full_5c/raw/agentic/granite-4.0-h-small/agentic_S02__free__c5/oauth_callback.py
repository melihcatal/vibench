import urllib.parse
import requests
import identity_client
import identity_models

# Concrete provider: Google Identity Platform (OAuth 2.0)
CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:5000/oauth_callback"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"


def fetch_tokens(code):
    """Exchange authorization code for access/refresh tokens."""
    payload = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    resp = requests.post(TOKEN_ENDPOINT, data=payload)
    resp.raise_for_status()
    return resp.json()


def fetch_user_profile(access_token):
    """Retrieve basic user info using access token."""
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(USERINFO_ENDPOINT, headers=headers)
    resp.raise_for_status()
    return resp.json()


def handle_callback(request):
    # Assume request contains query params `code`, `state`
    code = request.args.get("code")
    if not code:
        raise ValueError("No authorization code in request")
    tokens = fetch_tokens(code)
    profile = fetch_user_profile(tokens["access_token"])
    normalized = identity_models.UserProfile.from_google(profile)
    # Store tokens, profile, etc. as needed
    return normalized

if __name__ == "__main__":
    # Placeholder for a Flask/Django view; here we just show the helper calls
    pass
