import os
import boto3

# Set up the Cognito client
cognito_client = boto3.client(
    "cognito-idp",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def refresh_session(refresh_token):
    try:
        response = cognito_client.initiate_auth(
            ClientId=os.getenv("COGNITO_CLIENT_ID"),
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={"REFRESH_TOKEN": refresh_token},
        )
        return response
    except Exception as e:
        print(e)
