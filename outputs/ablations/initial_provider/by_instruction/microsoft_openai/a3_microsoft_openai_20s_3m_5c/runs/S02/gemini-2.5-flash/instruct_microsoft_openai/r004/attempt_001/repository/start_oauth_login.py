import os
import urllib.parse

# Microsoft Azure AD / OpenAI
AZURE_AD_TENANT_ID = os.environ.get("AZURE_AD_TENANT_ID")
AZURE_AD_CLIENT_ID = os.environ.get("AZURE_AD_CLIENT_ID")
AZURE_AD_REDIRECT_URI = os.environ.get("AZURE_AD_REDIRECT_URI")

def start_microsoft_oauth_login():
    """
    Constructs the authorization URL for Microsoft Azure AD (OAuth 2.0 authorization code flow).
    """
    if not all([AZURE_AD_TENANT_ID, AZURE_AD_CLIENT_ID, AZURE_AD_REDIRECT_URI]):
        raise ValueError("Missing Azure AD configuration environment variables.")

    base_url = f"https://login.microsoftonline.com/{AZURE_AD_TENANT_ID}/oauth2/v2.0/authorize"
    params = {
        "client_id": AZURE_AD_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": AZURE_AD_REDIRECT_URI,
        "response_mode": "query",
        "scope": "openid profile email User.Read", # Common scopes for user info
        "state": "random_state_string", # In a real app, generate and validate a unique state
        "prompt": "select_account"
    }
    query_string = urllib.parse.urlencode(params)
    authorization_url = f"{base_url}?{query_string}"
    return authorization_url

if __name__ == "__main__":
    login_url = start_microsoft_oauth_login()
    print(f"Microsoft Azure AD Authorization URL: {login_url}")
