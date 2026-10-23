import boto3

def start_oauth_login():
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        AuthFlow='USER_SRP_AUTH',
        AuthParameters={
            'USERNAME': 'user',
            'PASSWORD': 'password'
        },
        ClientId='your-client-id'
    )
    print(response)