import os
import requests
from identity_client import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_CALLBACK_URL
from identity_models import TokenResponse

def handle_oauth_callback(auth_code: str) -> TokenResponse:
    """Exchanges an authorization code for tokens using Auth0's token endpoint."""
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": AUTH0_CALLBACK_URL,
    }
    
    response = requests.post(token_url, headers=headers, data=payload)
    response.raise_for_status()
    
    token_data = response.json()
    return TokenResponse(
        access_token=token_data.get("access_token"),
        id_token=token_data.get("id_token"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type"),
        scope=token_data.get("scope")
    )

if __name__ == "__main__":
    # This is a placeholder for demonstration. In a real app, 'code' would come from the request.
    print("Simulating a callback. Please provide an authorization code from Auth0.")
    # example_auth_code = "YOUR_AUTH_CODE_HERE" 
    # try:
    #     tokens = handle_oauth_callback(example_auth_code)
    #     print("Tokens received:", tokens)
    # except requests.exceptions.HTTPError as e:
    #     print(f"Error exchanging code for tokens: {e}")
    #     print(f"Response: {e.response.text}")
