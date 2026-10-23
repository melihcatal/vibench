import requests
from identity_client import auth0_client
from identity_models import UserLoginRequest, AuthResponse

def email_password_login(email: str, password: str) -> AuthResponse:
    """
    Signs in a user with email and password and returns tokens using Auth0 Authentication API.
    """
    url = auth0_client.get_authentication_api_url("/oauth/token")
    headers = {"Content-Type": "application/json"}
    
    request_data = UserLoginRequest(email=email, password=password)
    request_data.client_id = auth0_client.client_id
    request_data.client_secret = auth0_client.client_secret
    
    response = requests.post(url, headers=headers, json=request_data.to_dict())
    response.raise_for_status()
    
    return AuthResponse(response.json())

if __name__ == "__main__":
    # Example Usage (requires AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET env vars)
    # user_email = "test_user@example.com"
    # user_password = "SecurePassword123!"
    # try:
    #     auth_tokens = email_password_login(user_email, user_password)
    #     print(f"Login successful. Access Token: {auth_tokens.access_token[:10]}..., Refresh Token: {auth_tokens.refresh_token[:10]}...")
    # except requests.exceptions.HTTPError as e:
    #     print(f"Error logging in: {e.response.text}")
    pass
