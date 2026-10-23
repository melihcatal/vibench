import boto3

from identity_client import get_cognito_client


def password_reset(email, config=None):
    client = get_cognito_client(config)
    response = client.forgot_password(ClientId=config['client_id'], Username=email)
    return {'message': 'Password reset initiated'}