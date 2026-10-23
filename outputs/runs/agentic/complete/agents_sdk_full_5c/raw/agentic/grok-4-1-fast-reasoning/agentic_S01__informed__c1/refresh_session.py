from identity_client import CognitoIdentityClient
from identity_models import parse_auth_result, UserTokens

def refresh_session(refresh_token: str) -> UserTokens:
    client = CognitoIdentityClient()
    response = client.client.initiate_auth(
        ClientId=client.app_client_id,
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={
            'REFRESH_TOKEN': refresh_token
        }
    )
    return parse_auth_result(response['AuthenticationResult'])