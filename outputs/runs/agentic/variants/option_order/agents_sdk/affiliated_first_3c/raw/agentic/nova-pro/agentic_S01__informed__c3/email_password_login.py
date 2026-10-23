import boto3

def email_password_login(email, password):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        ClientId='your-client-id',
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': email,
            'PASSWORD': password
        }
    )
    return response