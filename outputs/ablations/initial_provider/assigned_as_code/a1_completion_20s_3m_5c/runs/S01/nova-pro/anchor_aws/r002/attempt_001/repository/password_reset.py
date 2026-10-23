import boto3

from identity_client import get_cognito_client
from identity_models import ResetRequest


def password_reset(payload):
    client = get_cognito_client()
    request = ResetRequest(ClientId=client['client_id'], Username=payload['email'])
    response = client.forgot_password(**request.to_dict())
    return {'message': 'Password reset initiated'}