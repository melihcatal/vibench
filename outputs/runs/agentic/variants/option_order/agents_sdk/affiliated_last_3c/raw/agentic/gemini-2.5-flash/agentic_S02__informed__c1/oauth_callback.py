import os
import requests
import json
from identity_client import get_auth0_config

def handle_auth0_callback(authorization_code: str):
    config = get_auth0_config()
    domain = config["AUTH0_DOMAIN"]
    client_id = config["AUTH0_CLIENT_ID"]
    client_secret = config["AUTH0_CLIENT_SECRET"]
    redirect_uri = config["AUTH0_REDIRECT_URI"]

    token_url = f"https://{domain}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": authorization_code,
        "redirect_uri": redirect_uri,
    }

    try:
        response = requests.post(token_url, headers=headers, data=payload)
        response.raise_for_status()
        tokens = response.json()
        print("Successfully exchanged code for tokens.")
        return tokens
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens: {e}")
        return None

if __name__ == "__main__":
    # Example usage (replace with actual code from the callback URL)
    sample_code = os.environ.get("AUTH0_SAMPLE_CODE", "dummy_code_from_callback")
    if sample_code == "dummy_code_from_callback":
        print("Please set the AUTH0_SAMPLE_CODE environment variable with a real authorization code.")
    else:
        tokens_data = handle_auth0_callback(sample_code)
        if tokens_data:
            print(json.dumps(tokens_data, indent=2))
