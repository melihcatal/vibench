import os
import requests
import json

# Replace with your actual client ID, client secret, and redirect URI
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI", "http://localhost:8000/oauth_callback")

def exchange_code_for_tokens(auth_code: str):
    """Exchanges an authorization code for access and ID tokens from Google."""
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "code": auth_code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    try:
        response = requests.post(token_url, data=payload)
        response.raise_for_status() # Raise an exception for bad status codes
        tokens = response.json()
        return tokens
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens: {e}")
        return None

if __name__ == "__main__":
    # This part simulates receiving an authorization code from the redirect
    # In a real application, you would get this from the query parameters of the incoming request
    example_auth_code = "_YOUR_SIMULATED_AUTHORIZATION_CODE_"
    print(f"Attempting to exchange simulated code: {example_auth_code[:10]}...\n")

    tokens = exchange_code_for_tokens(example_auth_code)

    if tokens:
        print("Successfully received tokens:")
        print(json.dumps(tokens, indent=2))
        access_token = tokens.get("access_token")
        id_token = tokens.get("id_token")
        print(f"\nAccess Token: {access_token[:20]}..." if access_token else "No access token")
        print(f"ID Token: {id_token[:20]}..." if id_token else "No ID token")
    else:
        print("Failed to obtain tokens.")
