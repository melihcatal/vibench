from identity_client import CognitoIdentityClient
from identity_models import UserLoginRequest, UserLoginResponse


def email_password_login(email: str, password: str) -> dict:
    client = CognitoIdentityClient()
    request = UserLoginRequest(email=email, password=password)
    response = client.login_user(email=request.email, password=request.password)
    return UserLoginResponse(**response).dict()
