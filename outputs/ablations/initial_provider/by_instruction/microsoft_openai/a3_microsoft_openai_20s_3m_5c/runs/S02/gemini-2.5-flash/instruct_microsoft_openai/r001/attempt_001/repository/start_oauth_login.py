import os
import urllib.parse

MICROSOFT_CLIENT_ID = os.environ.get("MICROSOFT_CLIENT_ID")
MICROSOFT_TENANT_ID = os.environ.get("MICROSOFT_TENANT_ID", "common") # "common" for multi-tenant apps
MICROSOFT_REDIRECT_URI = os.environ.get("MICROSOFT_REDIRECT_URI")

MICROSOFT_AUTHORITY = f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}"
MICROSOFT_AUTHORIZE_ENDPOINT = f"{MICROSOFT_AUTHORITY}/oauth2/v2.0/authorize"

def start_microsoft_oauth_login(state: str, scope: str = "openid profile email") -> str:
    """
    Constructs the Microsoft OAuth login URL.
    """
    if not all([MICROSOFT_CLIENT_ID, MICROSOFT_REDIRECT_URI]):
        raise ValueError("MICROSOFT_CLIENT_ID and MICROSOFT_REDIRECT_URI must be set in environment variables.")

    params = {
        "client_id": MICROSOFT_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": MICROSOFT_REDIRECT_URI,
        "scope": scope,
        "state": state,
        "response_mode": "query"
    }
    query_string = urllib.parse.urlencode(params)
    return f"{MICROSOFT_AUTHORIZE_ENDPOINT}?{query_string}"

if __name__ == "__main__":
    # Example usage:
    # login_url = start_microsoft_oauth_login(state="a_random_state_string_for_csrf_protection")
    # print(f"Redirect to: {login_url}")
    pass
