import boto3


def password_reset(email):
    client = boto3.client("cognito-idp", region_name="us-west-2")
    response = client.forgot_password(ClientId="your_client_id", Username=email)
    return response
