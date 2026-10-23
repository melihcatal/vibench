import boto3

def refresh_session(refresh_token):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    try:
        response = client.initiate_auth(
            ClientId='YOUR_COGNITO_CLIENT_ID',
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={'REFRESH_TOKEN': refresh_token}
        )
        return response['AuthenticationResult']
    except client.exceptions.NotAuthorizedException as e:
        print(f'Refresh token is invalid: {e}')
        return None