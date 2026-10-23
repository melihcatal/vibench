import boto3

from identity_client import get_cognito_client
from identity_models import LoginRequest, LoginResponse


def email_password_login(payload):
    client = get_cognito_client()
    request = LoginRequest(ClientId=client['client_id'],
                           Username=payload['email'],
                           Password=payload['password'])
    response = client.initiate_auth(AuthFlow='USER_PASSWORD_AUTH', AuthParameters=request.to_dict())
    return LoginResponse.from_dict(response).to_dict()