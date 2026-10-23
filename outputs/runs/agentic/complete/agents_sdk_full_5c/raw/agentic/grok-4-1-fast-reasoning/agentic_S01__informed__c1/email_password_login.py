from identity_client import CognitoIdentityClient
from identity_models import parse_auth_result, UserTokens

def email_password_login(email: str, password: str) -> UserTokens:
    client = CognitoIdentityClient()
    response = client.client.initiate_auth(
        ClientId=client.app_client_id,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': email,
            'PASSWORD': password
        }
    )
    return parse_auth_result(response['AuthenticationResult'])