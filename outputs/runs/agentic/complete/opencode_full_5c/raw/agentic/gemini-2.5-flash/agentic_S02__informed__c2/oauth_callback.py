import os
import requests
import json

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")


def handle_oauth_callback(authorization_code: str):
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": authorization_code,
        "redirect_uri": AUTH0_CALLBACK_URL,
    }
    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Example usage:
    # Set environment variables AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_CALLBACK_URL
    # code = "YOUR_AUTHORIZATION_CODE"
    # tokens = handle_oauth_callback(code)
    # print(json.dumps(tokens, indent=2))
    pass
