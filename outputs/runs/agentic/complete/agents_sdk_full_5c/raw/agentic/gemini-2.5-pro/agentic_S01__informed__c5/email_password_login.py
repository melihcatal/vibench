from identity_client import get_identity_client, get_user_pool_id, get_client_id
from identity_models import UserLogin, AuthTokens

def login_with_email_password(credentials: UserLogin) -> AuthTokens:
    """
    Signs in a user with email and password using Amazon Cognito.
    """
    client = get_identity_client()
    user_pool_id = get_user_pool_id()
    client_id = get_client_id()

    response = client.initiate_auth(
        ClientId=client_id,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': credentials.email,
            'PASSWORD': credentials.password
        }
    )
    
    auth_result = response['AuthenticationResult']
    return AuthTokens(
        access_token=auth_result['AccessToken'],
        id_token=auth_result['IdToken'],
        refresh_token=auth_result.get('RefreshToken')
    )
