from boto3 import client

COGNITO_REGION = 'us-west-2'
COGNITO_USER_POOL_ID = 'us-west-2_examplePoolId'
COGNITO_CLIENT_ID = 'exampleClientId'

def get_cognito_client():
    return client('cognito-idp', region_name=COGNITO_REGION)

def initiate_auth(username, password):
    cognito_client = get_cognito_client()
    response = cognito_client.initiate_auth(
        ClientId=COGNITO_CLIENT_ID,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={'USERNAME': username, 'PASSWORD': password}
    )
    return response

def get_user(access_token):
    cognito_client = get_cognito_client()
    response = cognito_client.get_user(
        AccessToken=access_token
    )
    return response