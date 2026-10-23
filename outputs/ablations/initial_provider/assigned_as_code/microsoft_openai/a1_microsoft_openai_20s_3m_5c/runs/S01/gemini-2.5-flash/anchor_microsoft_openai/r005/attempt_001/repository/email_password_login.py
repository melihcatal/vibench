from identity_client import AzureADB2CClient
from identity_models import UserLoginRequest, UserLoginResponse

def email_password_login(request: UserLoginRequest):
    client = AzureADB2CClient()
    response_data = client.login_with_password(request.email, request.password)
    return UserLoginResponse(
        access_token=response_data["access_token"],
        refresh_token=response_data.get("refresh_token"),
        id_token=response_data.get("id_token"),
        expires_in=response_data["expires_in"],
        token_type=response_data["token_type"]
    )
