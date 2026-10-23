import os
import requests
import urllib.parse

MICROSOFT_CLIENT_ID = os.environ.get("MICROSOFT_CLIENT_ID")
MICROSOFT_CLIENT_SECRET = os.environ.get("MICROSOFT_CLIENT_SECRET")
MICROSOFT_TENANT_ID = os.environ.get("MICROSOFT_TENANT_ID", "common")
MICROSOFT_REDIRECT_URI = os.environ.get("MICROSOFT_REDIRECT_URI")

MICROSOFT_AUTHORITY = f"https://login.microsoftonline.com/{MICROSOFT_TENANT_ID}"
MICROSOFT_TOKEN_ENDPOINT = f"{MICROSOFT_AUTHORITY}/oauth2/v2.0/token"

def exchange_code_for_tokens(code: str, state: str) -> dict:
    """
    Exchanges the authorization code for access, ID, and refresh tokens from Microsoft Entra ID.
    """
    if not all([MICROSOFT_CLIENT_ID, MICROSOFT_CLIENT_SECRET, MICROSOFT_REDIRECT_URI]):
        raise ValueError("MICROSOFT_CLIENT_ID, MICROSOFT_CLIENT_SECRET, and MICROSOFT_REDIRECT_URI must be set in environment variables.")

    data = {
        "client_id": MICROSOFT_CLIENT_ID,
        "scope": "openid profile email offline_access",
        "code": code,
        "redirect_uri": MICROSOFT_REDIRECT_URI,
        "grant_type": "authorization_code",
        "client_secret": MICROSOFT_CLIENT_SECRET,
    }
    
    # In a real application, you would also verify the 'state' parameter here
    # to prevent CSRF attacks. For this example, we'll assume it's handled.

    response = requests.post(MICROSOFT_TOKEN_ENDPOINT, data=data)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Example usage:
    # auth_code = "<authorization_code_from_redirect>"
    # received_state = "<state_from_redirect>"
    # try:
    #     tokens = exchange_code_for_tokens(code=auth_code, state=received_state)
    #     print("Tokens:", tokens)
    # except requests.exceptions.RequestException as e:
    #     print(f"Error exchanging code: {e}")
    # except ValueError as e:
    #     print(f"Configuration error: {e}")
    pass
