import os
from identity_client import create_cognito_client, get_app_client_id

def email_password_login(email: str, password: str) -&gt; dict:
    client = create_cognito_client()
    client_id = get_app_client_id()
    resp = client.initiate_auth(
        ClientId=client_id,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': email.lower(),
            'PASSWORD': password,
        },
    )
    auth_result = resp['AuthenticationResult']
    return {
        'access_token': auth_result['AccessToken'],
        'id_token': auth_result['IdToken'],
        'refresh_token': auth_result['RefreshToken'],
        'expires_in': auth_result['ExpiresIn'],
        'token_type': auth_result['TokenType'],
    }