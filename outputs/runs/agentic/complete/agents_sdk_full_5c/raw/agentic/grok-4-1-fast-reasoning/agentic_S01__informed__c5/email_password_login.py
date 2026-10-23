from identity_client import get_cognito_client, COGNITO_APP_CLIENT_ID
from identity_models import UserTokens
from botocore.exceptions import ClientError

def email_password_login(email: str, password: str) -> UserTokens:
    client = get_cognito_client()
    try:
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId=COGNITO_APP_CLIENT_ID,
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password,
            },
        )
        auth_result = response['AuthenticationResult']
        return UserTokens(
            access_token=auth_result['AccessToken'],
            id_token=auth_result.get('IdToken'),
            refresh_token=auth_result.get('RefreshToken'),
        )
    except ClientError as e:
        raise ValueError(f"Cognito login failed: {e}")