import os
import requests
import json

# Google Identity Platform OAuth 2.0
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth_callback")
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

def exchange_code_for_tokens(auth_code: str) -> dict:
    data = {
        "code": auth_code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    try:
        response = requests.post(GOOGLE_TOKEN_URL, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error exchanging code for tokens: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage (replace with actual code from your web framework callback)
    # Simulating a callback with an authorization code
    example_auth_code = "4/0AZ4geWf..."
    print(f"Simulating token exchange for code: {example_auth_code}")
    tokens = exchange_code_for_tokens(example_auth_code)
    print(json.dumps(tokens, indent=2))
