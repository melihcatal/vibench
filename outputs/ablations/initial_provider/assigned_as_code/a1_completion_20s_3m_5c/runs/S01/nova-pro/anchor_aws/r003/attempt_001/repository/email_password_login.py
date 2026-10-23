import boto3

from identity_client import get_cognito_client
from identity_models import LoginRequest, LoginResponse


def email_password_login(email, password, config=None):
    client = get_cognito_client(config)
    request = LoginRequest(ClientId=config['client_id'], Username=email, Password=password)
    response = client.initiate_auth(AuthFlow='USER_PASSWORD_AUTH', AuthParameters=request.to_dict())
    return LoginResponse.from_dict(response).to_dict()