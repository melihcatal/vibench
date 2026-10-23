import boto3

def refresh_token(refresh_token, client_id, user_pool_id):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        ClientId=client_id,
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={'REFRESH_TOKEN': refresh_token}
    )
    return response['AuthenticationResult']
