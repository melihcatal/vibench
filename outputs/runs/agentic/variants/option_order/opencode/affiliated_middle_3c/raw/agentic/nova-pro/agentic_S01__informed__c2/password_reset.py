import os
import boto3

# Set up the Cognito client
cognito_client = boto3.client(
    "cognito-idp",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def password_reset(email):
    try:
        response = cognito_client.forgot_password(
            ClientId=os.getenv("COGNITO_CLIENT_ID"), Username=email
        )
        return response
    except Exception as e:
        print(e)
