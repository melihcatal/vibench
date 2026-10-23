from identity_client import AWSClient
from identity_models import RefreshSessionRequest, RefreshSessionResponse

def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    aws_client = AWSClient()
    cognito_client = aws_client.get_cognito_client()
    client_id = aws_client.get_client_id()

    try:
        response = cognito_client.initiate_auth(
            ClientId=client_id,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': request.refresh_token
            }
        )
        auth_result = response['AuthenticationResult']
        return RefreshSessionResponse(
            access_token=auth_result['AccessToken'],
            id_token=auth_result['IdToken'],
            expires_in=auth_result['ExpiresIn']
        )
    except cognito_client.exceptions.NotAuthorizedException:
        return RefreshSessionResponse(access_token="", id_token="", expires_in=0)
    except Exception as e:
        return RefreshSessionResponse(access_token="", id_token="", expires_in=0)
