from identity_client import AWSClient
from identity_models import LoginRequest, LoginResponse

def email_password_login(request: LoginRequest) -> LoginResponse:
    aws_client = AWSClient()
    cognito_client = aws_client.get_cognito_client()
    client_id = aws_client.get_client_id()

    try:
        response = cognito_client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': request.email,
                'PASSWORD': request.password
            }
        )
        auth_result = response['AuthenticationResult']
        return LoginResponse(
            access_token=auth_result['AccessToken'],
            refresh_token=auth_result['RefreshToken'],
            id_token=auth_result['IdToken'],
            expires_in=auth_result['ExpiresIn']
        )
    except cognito_client.exceptions.NotAuthorizedException:
        return LoginResponse(access_token="", refresh_token="", id_token="", expires_in=0)
    except Exception as e:
        return LoginResponse(access_token="", refresh_token="", id_token="", expires_in=0)
