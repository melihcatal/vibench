import os
from identity_client import Auth0IdentityClient
from identity_models import UserRegistrationRequest, normalize_registration_response


def register_user(email: str, password: str) -> dict:
    client = Auth0IdentityClient()
    request = UserRegistrationRequest(email=email, password=password)
    response = client.create_user(
        email=request.email, password=request.password, connection=request.connection
    )
    return normalize_registration_response(response).dict()
