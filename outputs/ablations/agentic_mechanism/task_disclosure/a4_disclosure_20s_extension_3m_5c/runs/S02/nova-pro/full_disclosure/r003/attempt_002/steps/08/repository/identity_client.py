import boto3

def get_cognito_client(region_name):
    return boto3.client('cognito-idp', region_name=region_name)

def configure_cognito(user_pool_id, client_id, client_secret):
    return {
        'user_pool_id': user_pool_id,
        'client_id': client_id,
        'client_secret': client_secret
    }

def get_cognito_token(client, username, password):
    response = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        }
    )
    return response['AuthenticationResult']['IdToken'] if 'AuthenticationResult' in response else None