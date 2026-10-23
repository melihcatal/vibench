import os
import requests
import json


def exchange_google_auth_code_for_tokens(
    code: str, client_id: str, client_secret: str, redirect_uri: str
) -> dict:
    """
    Exchanges the authorization code for access and ID tokens using Google OAuth 2.0.
    """
    token_url = "https://oauth2.googleapis.com/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Example usage (replace with actual values from identity_client.py and a real authorization code)
    AUTH_CODE = (
        "YOUR_AUTHORIZATION_CODE"  # This would come from the redirect from Google
    )
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get(
        "GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET"
    )
    GOOGLE_REDIRECT_URI = os.environ.get(
        "GOOGLE_REDIRECT_URI", "http://localhost:8080/oauth/callback/google"
    )

    if AUTH_CODE == "YOUR_AUTHORIZATION_CODE":
        print("Please provide a real authorization code to test this script.")
    else:
        try:
            tokens = exchange_google_auth_code_for_tokens(
                code=AUTH_CODE,
                client_id=GOOGLE_CLIENT_ID,
                client_secret=GOOGLE_CLIENT_SECRET,
                redirect_uri=GOOGLE_REDIRECT_URI,
            )
            print("Successfully exchanged code for tokens:")
            print(json.dumps(tokens, indent=2))
        except requests.exceptions.RequestException as e:
            print(f"Error exchanging code for tokens: {e}")
            if e.response:
                print(f"Response: {e.response.text}")
