import os
import requests
from urllib.parse import urlencode

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")


def exchange_code_for_tokens(authorization_code: str):
    """Exchanges an authorization code for access, ID, and refresh tokens with Auth0."""
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": authorization_code,
        "redirect_uri": AUTH0_CALLBACK_URL,
    }
    response = requests.post(token_url, headers=headers, data=urlencode(payload))
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # This is a placeholder for demonstration. In a real application, the code would come from the redirect.
    sample_code = "YOUR_AUTHORIZATION_CODE_HERE"
    try:
        tokens = exchange_code_for_tokens(sample_code)
        print("Successfully exchanged code for tokens.")
        print(tokens)
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens: {e}")
