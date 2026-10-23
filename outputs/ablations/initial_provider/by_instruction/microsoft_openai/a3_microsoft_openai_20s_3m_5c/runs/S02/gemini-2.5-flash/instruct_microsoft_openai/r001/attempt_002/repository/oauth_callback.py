import os
import httpx
import json

def exchange_microsoft_authorization_code(
    client_id: str,
    tenant_id: str,
    client_secret: str,
    redirect_uri: str,
    authorization_code: str
) -> dict:
    """
    Exchanges an authorization code for access and ID tokens with Microsoft Azure AD.
    """
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    token_endpoint = f"{authority}/oauth2/v2.0/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "client_id": client_id,
        "scope": "openid profile email User.Read",
        "code": authorization_code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "client_secret": client_secret,
    }

    try:
        response = httpx.post(token_endpoint, headers=headers, data=data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
        raise
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}.")
        raise

if __name__ == "__main__":
    # Example usage with placeholder environment variables
    CLIENT_ID = os.environ.get("AZURE_AD_CLIENT_ID", "YOUR_AZURE_AD_CLIENT_ID")
    TENANT_ID = os.environ.get("AZURE_AD_TENANT_ID", "YOUR_AZURE_AD_TENANT_ID")
    CLIENT_SECRET = os.environ.get("AZURE_AD_CLIENT_SECRET", "YOUR_AZURE_AD_CLIENT_SECRET")
    REDIRECT_URI = os.environ.get("AZURE_AD_REDIRECT_URI", "http://localhost:8000/oauth_callback")
    
    # This would typically come from the redirect after user login
    # For demonstration, we'll use a dummy code
    AUTH_CODE = "DUMMY_AUTHORIZATION_CODE" 

    if AUTH_CODE == "DUMMY_AUTHORIZATION_CODE":
        print("Please replace 'DUMMY_AUTHORIZATION_CODE' with a real authorization code obtained from the login flow.")
    else:
        try:
            tokens = exchange_microsoft_authorization_code(
                CLIENT_ID, TENANT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_CODE
            )
            print("Successfully exchanged code for tokens:")
            print(json.dumps(tokens, indent=2))
        except Exception as e:
            print(f"Failed to exchange authorization code: {e}")
