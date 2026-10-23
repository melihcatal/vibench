import os
import requests

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")


def start_oauth_login():
    auth_url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "client_id": AUTH0_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": "http://localhost:3000/callback",
        "scope": "openid profile email",
    }
    response = requests.get(auth_url, params=params)
    return response.url
