import boto3

def oauth_callback(code):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        AuthFlow='CUSTOM_AUTH',
        AuthParameters={
            'USERNAME': 'user',
            'PASSWORD': code
        },
        ClientId='your-client-id'
    )
    print(response)