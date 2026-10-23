import os
import requests
from identity_client import get_auth0_client
from identity_models import UserRegistrationRequest, UserRegistrationResponse


def register_user(
    email: str, password: str, name: str = None
) -> UserRegistrationResponse:
    """Register a new user with email and password using Auth0."""
    client = get_auth0_client()

    # Auth0 Management API endpoint for creating users
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")

    # Get management API token
    token_url = f"https://{domain}/oauth/token"
    token_payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": f"https://{domain}/api/v2/",
        "grant_type": "client_credentials",
    }

    token_response = requests.post(token_url, json=token_payload)
    token_response.raise_for_status()
    access_token = token_response.json()["access_token"]

    # Create user in Auth0
    create_user_url = f"https://{domain}/api/v2/users"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    user_data = {
        "email": email,
        "password": password,
        "connection": "Username-Password-Authentication",
        "email_verified": False,
    }

    if name:
        user_data["name"] = name

    response = requests.post(create_user_url, headers=headers, json=user_data)
    response.raise_for_status()

    user_info = response.json()

    return UserRegistrationResponse(
        user_id=user_info["user_id"],
        email=user_info["email"],
        email_verified=user_info.get("email_verified", False),
        created_at=user_info.get("created_at"),
    )
