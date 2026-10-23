import boto3

def oauth_callback(authorization_code):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        ClientId='YOUR_CLIENT_ID',
        AuthFlow='CUSTOM_AUTH',
        AuthParameters={'USERNAME': 'YOUR_USERNAME', 'ANSWER': authorization_code}
    )
    print(response)

if __name__ == '__main__':
    oauth_callback('YOUR_AUTHORIZATION_CODE')