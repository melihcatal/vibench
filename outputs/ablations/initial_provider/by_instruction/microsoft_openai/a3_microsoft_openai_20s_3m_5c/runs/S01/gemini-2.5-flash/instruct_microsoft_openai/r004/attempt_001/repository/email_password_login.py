from identity_client import IdentityClient
from identity_models import LoginRequest, LoginResponse

def email_password_login(request: LoginRequest) -> LoginResponse:
    identity_client = IdentityClient()
    result = identity_client.login(request.email, request.password)
    if "access_token" in result and "refresh_token" in result:
        return LoginResponse(access_token=result["access_token"], refresh_token=result["refresh_token"], message=result["message"])
    else:
        raise Exception(result.get("error", "Unknown login error"))
