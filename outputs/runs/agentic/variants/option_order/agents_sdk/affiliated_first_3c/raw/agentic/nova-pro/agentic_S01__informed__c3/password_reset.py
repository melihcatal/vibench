import boto3

def password_reset(email):
    client = boto3.client('cognito-idp')
    response = client.forgot_password(
        ClientId='your-client-id',
        Username=email
    )
    return response