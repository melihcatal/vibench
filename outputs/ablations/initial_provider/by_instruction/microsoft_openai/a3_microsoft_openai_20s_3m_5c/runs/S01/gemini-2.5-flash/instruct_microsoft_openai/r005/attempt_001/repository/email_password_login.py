from identity_models import LoginRequest, LoginResponse
from identity_client import IdentityClient

def email_password_login(request: LoginRequest) -> LoginResponse:
    identity_client = IdentityClient()
    login_result = identity_client.login(request.email, request.password)

    return LoginResponse(
        access_token=login_result["access_token"],
        refresh_token=login_result["refresh_token"],
        expires_in=login_result["expires_in"]
    )
