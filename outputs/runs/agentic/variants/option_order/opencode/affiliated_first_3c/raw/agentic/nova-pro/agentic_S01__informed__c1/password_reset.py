import boto3


def password_reset(username):
    client = boto3.client("cognito-idp", region_name="us-west-2")
    response = client.forgot_password(ClientId="your-client-id", Username=username)
    return response
