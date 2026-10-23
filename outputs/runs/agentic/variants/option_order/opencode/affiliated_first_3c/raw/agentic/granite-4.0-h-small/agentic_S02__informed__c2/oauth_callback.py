import os
import sys
import json
from urllib.parse import parse_qs
from identity_client import IdentityClient

# IBM App ID configuration
IBM_APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
IBM_APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")
TOKEN_ENDPOINT = "https://us-south.appid.cloud.ibm.com/oauth/v4/token"
REDIRECT_URI = "http://localhost:5000/oauth/callback"


def oauth_callback(request_params):
    """Handle OAuth callback, exchange authorization code for tokens, and extract profile claims.

    Args:
        request_params (dict): Parsed query parameters from the HTTP request (e.g., from Flask's request.args).
    """
    code = request_params.get("code")
    state = request_params.get("state")

    if not code:
        raise ValueError("Missing authorization code")

    client = IdentityClient(
        base_url=TOKEN_ENDPOINT,
        client_id=IBM_APPID_CLIENT_ID,
        client_secret=IBM_APPID_CLIENT_SECRET,
    )

    # Exchange code for access token, id token, and refresh token
    token_payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        # Include PKCE verifier if you generated one earlier:
        # 'code_verifier': generated_verifier,
    }
    response = client.post(json=token_payload)
    data = response.json()

    # Basic validation of state if you use it for CSRF protection
    if state and state != request_params.get("client_state"):
        raise ValueError("State mismatch - possible CSRF attack")

    # Extract tokens
    access_token = data.get("access_token")
    id_token = data.get("id_token")
    refresh_token = data.get("refresh_token")

    # Decode and normalize claims from ID token (simplified example)
    profile = client.decode_id_token(id_token)
    normalized_profile = {
        "sub": profile["sub"],
        "email": profile.get("email"),
        "name": profile.get("name"),
        "preferred_username": profile.get("preferred_username"),
        # Add any other standardized claim mappings here
    }
    return {
        "access_token": access_token,
        "id_token": id_token,
        "refresh_token": refresh_token,
        "profile": normalized_profile,
    }


if __name__ == "__main__":
    # Example usage for local testing - parse query string from argv
    query_string = sys.argv[1] if len(sys.argv) > 1 else ""
    params = dict(parse_qs(query_string))
    try:
        result = oauth_callback(params)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), indent=2)
