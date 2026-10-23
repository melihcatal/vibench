import os
import urllib.parse


def generate_google_oauth_url(
    client_id: str, redirect_uri: str, scope: list[str], state: str
) -> str:
    """
    Generates the Google OAuth 2.0 authorization URL for an authorization code flow.
    """
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(scope),
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"


if __name__ == "__main__":
    # Example usage (replace with actual client_id, redirect_uri, and scope from identity_client.py)
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
    GOOGLE_REDIRECT_URI = os.environ.get(
        "GOOGLE_REDIRECT_URI", "http://localhost:8080/oauth/callback/google"
    )
    GOOGLE_SCOPES = ["openid", "email", "profile"]
    LOGIN_STATE = "a_random_state_string"  # In a real app, this would be a securely generated unique value

    auth_url = generate_google_oauth_url(
        client_id=GOOGLE_CLIENT_ID,
        redirect_uri=GOOGLE_REDIRECT_URI,
        scope=GOOGLE_SCOPES,
        state=LOGIN_STATE,
    )
    print(f"Generated Google OAuth URL: {auth_url}")
