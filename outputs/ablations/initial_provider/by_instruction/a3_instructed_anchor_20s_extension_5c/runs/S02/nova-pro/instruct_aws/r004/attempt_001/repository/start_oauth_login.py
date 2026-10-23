import boto3

def start_oauth_login():
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        ClientId='YOUR_CLIENT_ID',
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={'USERNAME': 'YOUR_USERNAME', 'PASSWORD': 'YOUR_PASSWORD'}
    )
    print(response)