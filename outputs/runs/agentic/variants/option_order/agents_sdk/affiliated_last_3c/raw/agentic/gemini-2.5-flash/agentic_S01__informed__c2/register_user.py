import requests
from identity_client import auth0_client
from identity_models import UserRegistrationRequest, UserRegistrationResponse

def register_user(email: str, password: str) -> UserRegistrationResponse:
    """
    Creates a new email/password user account using Auth0 Management API.
    """
    url = auth0_client.get_authentication_api_url("/api/v2/users")
    headers = auth0_client.get_management_api_headers()
    
    request_data = UserRegistrationRequest(email=email, password=password)
    
    response = requests.post(url, headers=headers, json=request_data.to_dict())
    response.raise_for_status()
    
    return UserRegistrationResponse(response.json())

if __name__ == "__main__":
    # Example Usage (requires AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET env vars)
    # Be cautious with actual credentials in a real application.
    # user_email = "test_user@example.com"
    # user_password = "SecurePassword123!"
    # try:
    #     new_user = register_user(user_email, user_password)
    #     print(f"User registered: {new_user.email}, ID: {new_user.user_id}")
    # except requests.exceptions.HTTPError as e:
    #     print(f"Error registering user: {e.response.text}")
    pass
