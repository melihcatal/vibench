import boto3


def password_reset(email):
    client = boto3.client("cognito-idp", region_name="us-east-1")
    response = client.forgot_password(ClientId="your-client-id", Username=email)
    return response
