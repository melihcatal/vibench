import boto3

def register_user(username, password):
    client = boto3.client('cognito-idp')
    response = client.sign_up(
        ClientId='YOUR_COGNITO_CLIENT_ID',
        Username=username,
        Password=password
    )
    return response