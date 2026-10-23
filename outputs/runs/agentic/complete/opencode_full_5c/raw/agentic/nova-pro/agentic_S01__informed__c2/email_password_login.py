import os
import boto3


def email_password_login(email, password):
    cognito_client = boto3.client("cognito-idp", region_name="us-west-2")
    try:
        response = cognito_client.initiate_auth(
            ClientId=os.getenv("AWS_CLIENT_ID"),
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )
        return response
    except Exception as e:
        print(e)
