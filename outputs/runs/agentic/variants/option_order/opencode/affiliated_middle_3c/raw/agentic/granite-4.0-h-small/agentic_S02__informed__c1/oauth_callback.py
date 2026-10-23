import os
import urllib.parse
import sys
from identity_client import IdentityClient

# -------------- Amazon Cognito Hosted UI Federation --------------
# Reference: service=Amazon Cognito federation
COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")
COGNITO_CLIENT_SECRET = os.getenv("COGNITO_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8080/callback"

ALLOWED_CALLBACK_PATHS = ["/callback"]


def oauth_callback():
    """Exchange authorization code for tokens and return user info."""
    # Ensure request came from our redirect endpoint
    if len(sys.argv) < 2 or sys.argv[1] not in ALLOWED_CALLBACK_PATHS:
        print("Invalid redirect path", file=sys.stderr)
        sys.exit(1)

    # Parse query string from redirected URL (e.g., from unit test or mock)
    query = urllib.parse.parse_qs(sys.argv[2] if len(sys.argv) > 2 else "")
    code = query.get("code")
    if not code:
        print("No authorization code received", file=sys.stderr)
        sys.exit(1)

    client = IdentityClient(
        provider="cognito",
        domain=COGNITO_DOMAIN,
        client_id=COGNITO_CLIENT_ID,
        client_secret=COGNITO_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
    )
    tokens = client.exchange_code_for_tokens(code[0])

    # Normalized federated claims
    user_profile = client.fetch_user_profile(tokens["id_token"])
    print("Access Token:", tokens["access_token"])
    print(
        "Refresh Token:",
        tokens["refresh_token"] if "refresh_token" in tokens else "N/A",
    )
    print("User Profile:", user_profile)

    # Return JSON-friendly payload for downstream services
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens.get("refresh_token"),
        "id_token": tokens["id_token"],
        "user_profile": user_profile,
    }


if __name__ == "__main__":
    # For local testing: python oauth_callback.py /callback \"?code=ABC123\"
    oauth_callback()
