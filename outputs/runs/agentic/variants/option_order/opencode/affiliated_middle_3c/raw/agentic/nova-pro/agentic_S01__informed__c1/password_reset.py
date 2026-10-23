import boto3


def password_reset(email):
    cognito_client = boto3.client("cognito-idp")
    response = cognito_client.forgot_password(
        ClientId="YOUR_COGNITO_CLIENT_ID", Username=email
    )
    return response
