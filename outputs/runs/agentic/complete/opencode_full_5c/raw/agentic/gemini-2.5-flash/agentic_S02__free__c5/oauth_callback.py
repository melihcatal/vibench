import os
import requests
import json


def handle_auth0_callback(code: str) -> dict:
    """
    Handles the Auth0 callback, exchanging the authorization code for tokens.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.environ.get(
        "AUTH0_CLIENT_SECRET", "YOUR_AUTH0_CLIENT_SECRET"
    )
    AUTH0_CALLBACK_URL = os.environ.get(
        "AUTH0_CALLBACK_URL", "http://localhost:8000/callback"
    )

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/json"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": AUTH0_CALLBACK_URL,
    }

    try:
        response = requests.post(token_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        tokens = response.json()
        return tokens
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # This is an example. In a real application, the 'code' would come from the redirect.
    example_code = "YOUR_AUTHORIZATION_CODE_HERE"
    if example_code == "YOUR_AUTHORIZATION_CODE_HERE":
        print(
            "Please replace 'YOUR_AUTHORIZATION_CODE_HERE' with an actual authorization code."
        )
    else:
        result = handle_auth0_callback(example_code)
        print(json.dumps(result, indent=2))
