import os
import requests
from identity_client import AUTH0_DOMAIN, get_management_api_token
from identity_models import UserRegistrationRequest


def register_user(email: str, password: str) -> dict:
    """
    Registers a new user account with Auth0.
    """
    management_api_token = get_management_api_token()
    headers = {
        "Authorization": f"Bearer {management_api_token}",
        "Content-Type": "application/json",
    }
    user_registration_request = UserRegistrationRequest(email=email, password=password)
    create_user_url = f"https://{AUTH0_DOMAIN}/api/v2/users"

    response = requests.post(
        create_user_url, headers=headers, json=user_registration_request.to_dict()
    )
    response.raise_for_status()
    return response.json()
