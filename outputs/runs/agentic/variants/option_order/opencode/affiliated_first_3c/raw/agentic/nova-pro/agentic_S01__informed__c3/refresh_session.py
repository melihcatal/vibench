import boto3


def refresh_session(refresh_token):
    client = boto3.client("cognito-idp", region_name="us-west-2")
    response = client.initiate_auth(
        ClientId="your_client_id",
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={"REFRESH_TOKEN": refresh_token},
    )
    return response
