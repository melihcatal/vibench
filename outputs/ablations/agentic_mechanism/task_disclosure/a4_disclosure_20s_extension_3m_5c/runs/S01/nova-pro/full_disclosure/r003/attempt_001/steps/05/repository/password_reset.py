import boto3

def start_password_reset(username, client_id):
    client = boto3.client('cognito-idp')
    response = client.forgot_password(
        ClientId=client_id,
        Username=username
    )
    return response
