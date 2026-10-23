import os
import urllib.parse

def start_microsoft_oauth_login(client_id: str, tenant_id: str, redirect_uri: str, scope: list[str]) -> str:
    """
    Starts an OAuth 2.0 authorization-code login flow with Microsoft Azure AD.
    """
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    authorization_endpoint = f"{authority}/oauth2/v2.0/authorize"

    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": " ".join(scope),
        "response_mode": "query",
        "prompt": "select_account",
    }
    return f"{authorization_endpoint}?{urllib.parse.urlencode(params)}"

if __name__ == "__main__":
    # Example usage with placeholder environment variables
    CLIENT_ID = os.environ.get("AZURE_AD_CLIENT_ID", "YOUR_AZURE_AD_CLIENT_ID")
    TENANT_ID = os.environ.get("AZURE_AD_TENANT_ID", "YOUR_AZURE_AD_TENANT_ID")
    REDIRECT_URI = os.environ.get("AZURE_AD_REDIRECT_URI", "http://localhost:8000/oauth_callback")
    SCOPES = ["openid", "profile", "email", "User.Read"]

    login_url = start_microsoft_oauth_login(CLIENT_ID, TENANT_ID, REDIRECT_URI, SCOPES)
    print(f"Please visit this URL to log in: {login_url}")
