import boto3


def refresh_session(refresh_token):
    cognito_client = boto3.client("cognito-idp")
    response = cognito_client.initiate_auth(
        ClientId="YOUR_COGNITO_CLIENT_ID",
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={"REFRESH_TOKEN": refresh_token},
    )
    return response
