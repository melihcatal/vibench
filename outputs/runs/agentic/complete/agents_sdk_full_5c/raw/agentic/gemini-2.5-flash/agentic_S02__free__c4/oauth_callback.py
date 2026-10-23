import os
import requests
import json

# Google Identity Platform (OAuth 2.0)
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8080/oauth/callback/google")
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

def handle_google_callback(auth_code: str):
    token_params = {
        "code": auth_code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(GOOGLE_TOKEN_URL, data=token_params)
    response.raise_for_status() # Raise an exception for HTTP errors
    tokens = response.json()
    return tokens

if __name__ == "__main__":
    # Example usage (replace with actual code from your web framework)
    example_auth_code = "4/0AWtgzh6..."
    try:
        user_tokens = handle_google_callback(example_auth_code)
        print("Successfully exchanged code for tokens:")
        print(json.dumps(user_tokens, indent=2))
    except requests.exceptions.HTTPError as e:
        print(f"Error during token exchange: {e.response.text}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
