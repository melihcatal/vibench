import boto3

def password_reset(email):
    client = boto3.client('cognito-idp')
    response = client.forgot_password(
        ClientId='YOUR_COGNITO_CLIENT_ID',
        Username=email
    )
    return response