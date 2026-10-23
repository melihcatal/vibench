from boto3 import client

COGNITO_USER_POOL_ID = 'your-user-pool-id'
COGNITO_CLIENT_ID = 'your-client-id'
COGNITO_CLIENT_SECRET = 'your-client-secret'

def get_cognito_client():
    return client(
        'cognito-idp',
        region_name='us-east-1',
        aws_access_key_id='your-access-key-id',
        aws_secret_access_key='your-secret-access-key'
    )

def sign_in_user(username, password):
    cognito_client = get_cognito_client()
    response = cognito_client.initiate_auth(
        ClientId=COGNITO_CLIENT_ID,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={'USERNAME': username, 'PASSWORD': password}
    )
    return response

def sign_up_user(username, password, user_attributes):
    cognito_client = get_cognito_client()
    response = cognito_client.sign_up(
        ClientId=COGNITO_CLIENT_ID,
        Username=username,
        Password=password,
        UserAttributes=user_attributes
    )
    return response

def confirm_sign_up(username, confirmation_code):
    cognito_client = get_cognito_client()
    response = cognito_client.confirm_sign_up(
        ClientId=COGNITO_CLIENT_ID,
        Username=username,
        ConfirmationCode=confirmation_code
    )
    return response