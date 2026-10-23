import boto3

# Configuration for Amazon Cognito
COGNITO_REGION = 'us-east-1'
COGNITO_USER_POOL_ID = 'us-east-1_XXXXXXXXX'
COGNITO_APP_CLIENT_ID = 'XXXXXXXXXXXXXXXXXXXX'

def get_cognito_client():
    return boto3.client('cognito-idp', region_name=COGNITO_REGION)

def initiate_auth(username, password):
    client = get_cognito_client()
    response = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        },
        ClientId=COGNITO_APP_CLIENT_ID
    )
    return response