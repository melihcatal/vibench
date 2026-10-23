import os
from google.oauth2 import id_token
from google.auth.transport import requests
import json

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")

def fetch_and_normalize_google_profile_claims(id_token_jwt):
    try:
        # Verify the ID token and get the claims
        id_info = id_token.verify_oauth2_token(id_token_jwt, requests.Request(), GOOGLE_CLIENT_ID)

        # Normalize claims to a common format
        normalized_claims = {
            "provider": "google",
            "sub": id_info.get("sub"),
            "email": id_info.get("email"),
            "email_verified": id_info.get("email_verified"),
            "name": id_info.get("name"),
            "given_name": id_info.get("given_name"),
            "family_name": id_info.get("family_name"),
            "picture": id_info.get("picture"),
            "locale": id_info.get("locale"),
        }
        return normalized_claims
    except ValueError as e:
        print(f"Error verifying ID token: {e}")
        return None

if __name__ == "__main__":
    # This is a minimal example. In a real application, you would get the ID token
    # from the session after a successful OAuth callback.
    # For demonstration, we'll simulate an ID token (replace with a real one for testing).
    # You can get a test ID token by completing the OAuth flow and inspecting the 'id_token' field.
    # Example: run start_oauth_login.py, complete login, then capture the ID token from the callback.
    sample_id_token_jwt = "YOUR_GOOGLE_ID_TOKEN_JWT_HERE"
    if sample_id_token_jwt == "YOUR_GOOGLE_ID_TOKEN_JWT_HERE":
        print("Please replace 'YOUR_GOOGLE_ID_TOKEN_JWT_HERE' with a valid Google ID Token JWT for testing.")
    else:
        claims = fetch_and_normalize_google_profile_claims(sample_id_token_jwt)
        if claims:
            print("Normalized Claims:")
            print(json.dumps(claims, indent=2))
        else:
            print("Failed to fetch or normalize claims.")
