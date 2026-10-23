
import os
import requests
from identity_client import IdentityClient
from identity_models import OAuthTokens

def handle_oauth_callback(code: str, state: str, code_verifier: str = None) -> OAuthTokens:
    client = IdentityClient()

    # In a real application, 'state' would be validated against the one stored in a cookie/session.
    # For simplicity, we are skipping state validation here.

    token_url = client.get_token_url()
    
    data = {
        "client_id": client.client_id,
        "scope": client.scope,
        "code": code,
        "redirect_uri": client.redirect_uri,
        "grant_type": "authorization_code",
    }
    
    if client.client_secret:
        data["client_secret"] = client.client_secret
    
    if code_verifier:
        data["code_verifier"] = code_verifier

    response = requests.post(token_url, data=data)
    response.raise_for_status()
    token_data = response.json()

    # Microsoft identity platform specific claim for token type, often 'Bearer'
    token_type = token_data.get("token_type", "Bearer") 

    tokens = OAuthTokens(
        access_token=token_data["access_token"],
        token_type=token_type,
        expires_in=token_data["expires_in"],
        refresh_token=token_data.get("refresh_token"),
        scope=token_data.get("scope"),
        id_token=token_data.get("id_token"),
    )
    print(f"Successfully exchanged code for tokens. Access Token (first 10 chars): {tokens.access_token[:10]}...")
    return tokens

if __name__ == '__main__':
    # Example usage: These would typically come from the redirect URL parameters
    # os.environ['AZURE_AD_CLIENT_ID'] = 'YOUR_AZURE_AD_CLIENT_ID'
    # os.environ['AZURE_AD_CLIENT_SECRET'] = 'YOUR_AZURE_AD_CLIENT_SECRET' # Only if not a public client
    # os.environ['AZURE_AD_REDIRECT_URI'] = 'http://localhost:5000/callback'

    # Placeholder values for demonstration
    example_code = "dummy_authorization_code"
    example_state = "dummy_state"
    try:
        # In a real scenario, you'd get the code from the request parameters
        # tokens = handle_oauth_callback(example_code, example_state)
        # print(tokens)
        print("Run this from a web framework with actual code and state parameters.")
    except requests.exceptions.HTTPError as e:
        print(f"Error during token exchange: {e.response.text}")

