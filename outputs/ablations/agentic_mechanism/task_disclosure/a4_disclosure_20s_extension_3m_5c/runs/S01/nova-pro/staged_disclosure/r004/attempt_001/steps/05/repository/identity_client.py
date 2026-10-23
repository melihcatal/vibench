import boto3

# Configuration
AWS_REGION = 'us-west-2'
USER_POOL_ID = 'us-west-2_XXXXXXXX'
CLIENT_ID = 'XXXXXXXXXXXXXXXXXXXXXXXX'

# Initialize Cognito client
cognito_client = boto3.client('cognito-idp', region_name=AWS_REGION)

# Helper functions
def sign_up(username, password, user_attributes):
    try:
        response = cognito_client.sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=user_attributes
        )
        return response
    except Exception as e:
        print(e)

def confirm_sign_up(username, confirmation_code):
    try:
        response = cognito_client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            ConfirmationCode=confirmation_code
        )
        return response
    except Exception as e:
        print(e)

def initiate_auth(username, password):
    try:
        response = cognito_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={'USERNAME': username, 'PASSWORD': password}
        )
        return response
    except Exception as e:
        print(e)

def delete_user(access_token):
    try:
        response = cognito_client.delete_user(
            AccessToken=access_token
        )
        return response
    except Exception as e:
        print(e)