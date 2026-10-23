import os
import boto3

# Set up the Cognito client
cognito_client = boto3.client(
    "cognito-idp",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def register_user(email, password):
    try:
        response = cognito_client.sign_up(
            ClientId=os.getenv("COGNITO_CLIENT_ID"),
            Username=email,
            Password=password,
            UserAttributes=[{"Name": "email", "Value": email}],
        )
        return response
    except Exception as e:
        print(e)
