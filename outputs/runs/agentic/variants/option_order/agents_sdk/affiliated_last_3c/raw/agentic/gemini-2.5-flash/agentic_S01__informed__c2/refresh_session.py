import requests
from identity_client import auth0_client
from identity_models import TokenRefreshRequest, AuthResponse

def refresh_session(refresh_token: str) -> AuthResponse:
    """
    Refreshes an expired session or access token using Auth0 Authentication API.
    """
    url = auth0_client.get_authentication_api_url("/oauth/token")
    headers = {"Content-Type": "application/json"}
    
    request_data = TokenRefreshRequest(refresh_token=refresh_token)
    request_data.client_id = auth0_client.client_id
    request_data.client_secret = auth0_client.client_secret
    
    response = requests.post(url, headers=headers, json=request_data.to_dict())
    response.raise_for_status()
    
    return AuthResponse(response.json())

if __name__ == "__main__":
    # Example Usage (requires AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET and a valid refresh token)
    # stored_refresh_token = "YOUR_VALID_REFRESH_TOKEN_HERE"
    # try:
    #     new_tokens = refresh_session(stored_refresh_token)
    #     print(f"Session refreshed. New Access Token: {new_tokens.access_token[:10]}...")
    # except requests.exceptions.HTTPError as e:
    #     print(f"Error refreshing session: {e.response.text}")
    pass
