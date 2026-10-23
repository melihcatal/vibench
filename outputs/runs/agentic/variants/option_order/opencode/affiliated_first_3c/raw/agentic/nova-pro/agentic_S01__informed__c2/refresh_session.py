import boto3


def refresh_session(refresh_token):
    client = boto3.client("cognito-idp", region_name="us-east-1")
    response = client.initiate_auth(
        ClientId="your-client-id",
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={"REFRESH_TOKEN": refresh_token},
    )
    return response
