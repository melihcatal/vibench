from boto3 import client

# Configuration variables
COGNITO_REGION = 'us-west-2'
COGNITO_USER_POOL_ID = 'us-west-2_abcdefghi'
COGNITO_CLIENT_ID = '1example23456789'

# Client helper utilities
def get_cognito_client():
    return client('cognito-idp', region_name=COGNITO_REGION)

def initiate_auth(username, password):
    cognito_client = get_cognito_client()
    response = cognito_client.initiate_auth(
        ClientId=COGNITO_CLIENT_ID,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        }
    )
    return response

def refresh_tokens(refresh_token):
    cognito_client = get_cognito_client()
    response = cognito_client.initiate_auth(
        ClientId=COGNITO_CLIENT_ID,
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={
            'REFRESH_TOKEN': refresh_token
        }
    )
    return response