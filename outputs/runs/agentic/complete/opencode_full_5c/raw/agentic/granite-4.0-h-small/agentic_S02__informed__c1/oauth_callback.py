import os
import requests
from identity_client import IdentityClient
from identity_models import TokenResponse


def exchange_code_for_tokens(
    code: str, redirect_uri: str, client_id: str, client_secret: str
) -> TokenResponse:
    """Exchange an authorization code for access and ID tokens using Google Identity Platform OIDC.

    Sends a POST request to Google's token endpoint with the required parameters.
    Expected environment variables:
        GOOGLE_CLIENT_ID       - OAuth client ID
        GOOGLE_CLIENT_SECRET   - OAuth client secret
        GOOGLE_TOKEN_URI       - token endpoint (default)
    Returns a TokenResponse object containing access_token, id_token, refresh_token.
    """
    token_uri = os.getenv("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token")
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_uri, data=data)
    response.raise_for_status()
    payload = response.json()
    return TokenResponse(**payload)


# Example usage (from a web framework route)
# code = request.args.get('code')
# redirect_uri = request.host_url + 'oauth_callback'
# client_id = os.getenv('GOOGLE_CLIENT_ID')
# client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
# token_resp = exchange_code_for_tokens(code, redirect_uri, client_id, client_secret)
# print(token_resp.access_token)

# TokenResponse model for consistent fields
# class TokenResponse:
#     access_token: str
#     id_token: str
#     refresh_token: str
#     expires_in: int = None
#     token_type: str = "Bearer"
