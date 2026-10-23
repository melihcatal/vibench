import boto3

def refresh_session(token):
    client = boto3.client('cognito-idp', region_name='us-west-2')
    response = client.initiate_auth(
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={'REFRESH_TOKEN': token}
    )
    return response['AuthenticationResult']