import os
import boto3


def password_reset(email):
    cognito_client = boto3.client("cognito-idp", region_name="us-west-2")
    try:
        response = cognito_client.forgot_password(
            ClientId=os.getenv("AWS_CLIENT_ID"), Username=email
        )
        return response
    except Exception as e:
        print(e)
