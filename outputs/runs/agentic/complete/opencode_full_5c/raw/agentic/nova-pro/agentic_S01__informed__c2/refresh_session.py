import os
import boto3


def refresh_session(refresh_token):
    cognito_client = boto3.client("cognito-idp", region_name="us-west-2")
    try:
        response = cognito_client.initiate_auth(
            ClientId=os.getenv("AWS_CLIENT_ID"),
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={"REFRESH_TOKEN": refresh_token},
        )
        return response
    except Exception as e:
        print(e)
