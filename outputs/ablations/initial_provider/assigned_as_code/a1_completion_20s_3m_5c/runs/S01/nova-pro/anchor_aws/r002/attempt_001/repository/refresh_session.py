import boto3

from identity_client import get_cognito_client
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(payload):
    client = get_cognito_client()
    request = RefreshRequest(ClientId=client['client_id'],
                             RefreshToken=payload['refresh_token'])
    response = client.initiate_auth(AuthFlow='REFRESH_TOKEN_AUTH', AuthParameters=request.to_dict())
    return RefreshResponse.from_dict(response).to_dict()