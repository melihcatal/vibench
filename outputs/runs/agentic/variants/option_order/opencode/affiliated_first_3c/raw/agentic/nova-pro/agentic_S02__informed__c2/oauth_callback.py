import boto3

COGNITO_CLIENT_ID = "your-cognito-client-id"


def oauth_callback(code):
    client = boto3.client("cognito-idp")
    response = client.initiate_auth(
        AuthFlow="CUSTOM_AUTH",
        AuthParameters={"CODE": code},
        ClientId=COGNITO_CLIENT_ID,
    )
    return response
