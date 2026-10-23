import os
import requests
from identity_client import Auth0Client
from identity_models import UserRegistrationRequest, UserRegistrationResponse


def register_user(email: str, password: str) -> UserRegistrationResponse:
    client = Auth0Client()
    url = f"https://{client.domain}/dbconnections/signup"
    payload = UserRegistrationRequest(
        email=email, password=password, connection=client.connection
    ).dict()

    response = requests.post(url, json=payload, headers=client.headers)
    response.raise_for_status()
    data = response.json()

    return UserRegistrationResponse(
        user_id=data["_id"], email=data["email"], email_verified=data["email_verified"]
    )
