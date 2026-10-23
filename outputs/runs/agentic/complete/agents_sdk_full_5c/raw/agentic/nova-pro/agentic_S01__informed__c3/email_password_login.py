import boto3

def email_password_login(username, password):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        ClientId='YOUR_COGNITO_CLIENT_ID',
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        }
    )
    return response