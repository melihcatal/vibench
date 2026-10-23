import os
from identity_client import create_cognito_client, get_app_client_id

def refresh_session(refresh_token: str) -&gt; dict:
    client = create_cognito_client()
    client_id = get_app_client_id()
    resp = client.initiate_auth(
        ClientId=client_id,
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={
            'REFRESH_TOKEN': refresh_token,
        },
    )
    auth_result = resp['AuthenticationResult']
    return {
        'access_token': auth_result['AccessToken'],
        'id_token': auth_result.get('IdToken'),
        'expires_in': auth_result['ExpiresIn'],
        'token_type': auth_result['TokenType'],
    }