import os
import requests
import json

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")

def handle_callback(code: str):
    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_CALLBACK_URL]):
        raise ValueError("Missing Auth0 configuration environment variables.")

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    payload = {
        'grant_type': 'authorization_code',
        'client_id': AUTH0_CLIENT_ID,
        'client_secret': AUTH0_CLIENT_SECRET,
        'code': code,
        'redirect_uri': AUTH0_CALLBACK_URL
    }

    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()
    tokens = response.json()
    return tokens

if __name__ == '__main__':
    # Example usage (simulate an authorization code):
    # export AUTH0_DOMAIN="YOUR_AUTH0_DOMAIN"
    # export AUTH0_CLIENT_ID="YOUR_AUTH0_CLIENT_ID"
    # export AUTH0_CLIENT_SECRET="YOUR_AUTH0_CLIENT_SECRET"
    # export AUTH0_CALLBACK_URL="http://localhost:8000/callback"
    # auth_code = "mock_authorization_code_from_redirect"
    # try:
    #     user_tokens = handle_callback(auth_code)
    #     print("Successfully exchanged code for tokens:")
    #     print(json.dumps(user_tokens, indent=2))
    # except Exception as e:
    #     print(f"Error handling callback: {e}")
    pass
