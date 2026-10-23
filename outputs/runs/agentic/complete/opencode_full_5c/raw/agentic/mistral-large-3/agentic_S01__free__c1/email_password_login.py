import os
from identity_client import Auth0IdentityClient
from identity_models import UserLoginRequest, normalize_login_response


def email_password_login(email: str, password: str) -> dict:
    client = Auth0IdentityClient()
    request = UserLoginRequest(email=email, password=password)
    response = client.login_user(
        email=request.email, password=request.password, realm=request.realm
    )
    return normalize_login_response(response).dict()
