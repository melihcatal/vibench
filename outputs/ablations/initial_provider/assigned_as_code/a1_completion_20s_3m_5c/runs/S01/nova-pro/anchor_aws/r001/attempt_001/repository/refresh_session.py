import boto3

def refresh_session(refresh_token, config=None):
    config = config or {}
    client = boto3.client('cognito-idp', region_name=config.get('region'))
    response = client.initiate_auth(
        ClientId=config['client_id'],
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={'REFRESH_TOKEN': refresh_token}
    )
    return {'access_token': response['AuthenticationResult']['AccessToken'],
            'refresh_token': response['AuthenticationResult']['RefreshToken']}
