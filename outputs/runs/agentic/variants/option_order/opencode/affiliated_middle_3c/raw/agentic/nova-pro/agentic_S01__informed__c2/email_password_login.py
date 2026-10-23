import os
import boto3

# Set up the Cognito client
cognito_client = boto3.client(
    "cognito-idp",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def email_password_login(email, password):
    try:
        response = cognito_client.initiate_auth(
            ClientId=os.getenv("COGNITO_CLIENT_ID"),
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )
        return response
    except Exception as e:
        print(e)
