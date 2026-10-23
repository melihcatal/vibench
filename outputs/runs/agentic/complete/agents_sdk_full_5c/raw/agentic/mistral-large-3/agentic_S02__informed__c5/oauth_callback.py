import os
import requests
from typing import Dict, Optional

# Auth0 Authentication API
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI")

def exchange_code_for_tokens(code: str) -> Optional[Dict]:
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": AUTH0_REDIRECT_URI,
    }
    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    return response.json()