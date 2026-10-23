import boto3

def oauth_callback(code):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        AuthFlow='CUSTOM_AUTH',
        AuthParameters={'USERNAME': 'username', 'PASSWORD': 'password', 'SECRET_HASH': 'secret-hash'},
        ClientId='your-client-id',
        Session='session'
    )
    print(response)