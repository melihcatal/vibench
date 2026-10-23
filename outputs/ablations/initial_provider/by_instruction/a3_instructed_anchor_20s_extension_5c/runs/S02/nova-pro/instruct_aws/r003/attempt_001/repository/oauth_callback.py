import boto3

def oauth_callback(code):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        ClientId='YOUR_CLIENT_ID',
        AuthFlow='CUSTOM_AUTH',
        AuthParameters={'USERNAME': 'YOUR_USERNAME', 'ANSWER': code}
    )
    print(response)