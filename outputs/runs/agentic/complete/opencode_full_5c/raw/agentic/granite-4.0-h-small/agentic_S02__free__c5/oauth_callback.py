import os
import requests
from urllib.parse import parse_qs

# Provider: Auth0
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-tenant.auth0.com")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "http://localhost:5000/callback")

TOKEN_ENDPOINT = f"https://{AUTH0_DOMAIN}/oauth/token"


# Exchange code for tokens
def handle_callback(code):
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    resp = requests.post(TOKEN_ENDPOINT, data=token_data)
    resp.raise_for_status()
    tokens = resp.json()
    print("Access Token:", tokens.get("access_token"))
    print("ID Token:", tokens.get("id_token"))
    return tokens


if __name__ == "__main__":
    # Parse code from query string
    query = parse_qs(os.getenv("QUERY_STRING"))
    auth_code = query.get("code", [None])[0]
    if not auth_code:
        raise ValueError("No authorization code found")
    handle_callback(auth_code)
