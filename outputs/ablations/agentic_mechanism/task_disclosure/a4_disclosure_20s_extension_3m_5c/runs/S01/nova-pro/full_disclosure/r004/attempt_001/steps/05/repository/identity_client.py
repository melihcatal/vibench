import boto3

cognito_client = boto3.client('cognito-idp')

def configure_cognito(region, user_pool_id, app_client_id):
    cognito_client.meta.region_name = region
    return user_pool_id, app_client_id

def initiate_auth(username, password, user_pool_id, app_client_id):
    response = cognito_client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={'USERNAME': username, 'PASSWORD': password},
        ClientId=app_client_id
    )
    return response

def confirm_sign_up(username, confirmation_code, user_pool_id, app_client_id):
    response = cognito_client.confirm_sign_up(
        ClientId=app_client_id,
        SecretHash='',
        Username=username,
        ConfirmationCode=confirmation_code
    )
    return response

def resend_confirmation_code(username, user_pool_id, app_client_id):
    response = cognito_client.resend_confirmation_code(
        ClientId=app_client_id,
        SecretHash='',
        Username=username
    )
    return response