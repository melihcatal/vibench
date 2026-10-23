import boto3

COGNITO_DOMAIN = "your-cognito-domain"
COGNITO_CLIENT_ID = "your-cognito-client-id"


def start_oauth_login():
    client = boto3.client("cognito-idp")
    response = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": "username", "PASSWORD": "password"},
        ClientId=COGNITO_CLIENT_ID,
    )
    return response
