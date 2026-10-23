"""
Handles the callback from an Auth0 OAuth 2.0 flow.
"""
import os
from identity_client import get_auth0_client

def exchange_code_for_token(authorization_code: str):
    """
    Exchanges an authorization code for an access token and ID token.

    Args:
        authorization_code: The code received from the Auth0 callback.

    Returns:
        A dictionary containing the token information.
    """
    auth0 = get_auth0_client()
    redirect_uri = os.environ.get("AUTH0_CALLBACK_URL")

    # The Auth0 SDK handles the token exchange
    token_payload = auth0.authentication.get_token(
        code=authorization_code,
        grant_type='authorization_code',
        redirect_uri=redirect_uri,
    )
    return token_payload

# Example of how to handle the callback:
# if __name__ == "__main__":
#     # In a real web app, this code would be retrieved from the query params
#     auth_code = "example_auth_code" 
#     try:
#         tokens = exchange_code_for_token(auth_code)
#         print("Successfully exchanged code for tokens:")
#         print(tokens)
#     except Exception as e:
#         print(f"Error exchanging code: {e}")
