import os
import boto3


def register_user(email, password):
    cognito_client = boto3.client("cognito-idp", region_name="us-west-2")
    try:
        response = cognito_client.sign_up(
            ClientId=os.getenv("AWS_CLIENT_ID"),
            Username=email,
            Password=password,
            UserAttributes=[{"Name": "email", "Value": email}],
        )
        return response
    except Exception as e:
        print(e)
