import boto3


def password_reset(username):
    client = boto3.client("cognito-idp", region_name="us-east-1")
    response = client.forgot_password(
        ClientId="YOUR_COGNITO_CLIENT_ID", Username=username
    )
    return response
