import os
import requests
import json

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")


def handle_oauth_callback(code):
    if not all(
        [AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_CALLBACK_URL]
    ):
        raise ValueError("Missing Auth0 configuration environment variables.")

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": AUTH0_CALLBACK_URL,
    }

    try:
        response = requests.post(token_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging authorization code: {e}")
        return None


if __name__ == "__main__":
    # Example usage (replace with actual code from your application's callback handler)
    auth_code = "YOUR_AUTHORIZATION_CODE_HERE"
    tokens = handle_oauth_callback(auth_code)
    if tokens:
        print(json.dumps(tokens, indent=2))
