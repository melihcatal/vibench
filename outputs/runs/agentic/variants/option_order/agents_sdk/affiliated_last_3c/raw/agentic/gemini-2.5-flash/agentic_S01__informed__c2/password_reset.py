import requests
from identity_client import auth0_client
from identity_models import PasswordResetRequest

def password_reset(email: str) -> dict:
    """
    Starts a password reset flow for a local account using Auth0 Authentication API.
    """
    url = auth0_client.get_authentication_api_url("/dbconnections/change_password")
    headers = {"Content-Type": "application/json"}
    
    request_data = PasswordResetRequest(email=email)
    request_data.client_id = auth0_client.client_id
    
    response = requests.post(url, headers=headers, json=request_data.to_dict())
    response.raise_for_status()
    
    # Auth0 returns a simple message on success
    return {"message": response.text}

if __name__ == "__main__":
    # Example Usage (requires AUTH0_DOMAIN, AUTH0_CLIENT_ID env var)
    # user_email = "test_user@example.com"
    # try:
    #     result = password_reset(user_email)
    #     print(f"Password reset initiated for {user_email}: {result['message']}")
    # except requests.exceptions.HTTPError as e:
    #     print(f"Error initiating password reset: {e.response.text}")
    pass
