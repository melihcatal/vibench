import boto3

from identity_client import aws_region, cognito_client_id
from identity_models import RefreshRequest


def refresh_session(refresh_token: str):
    req = RefreshRequest(refresh_token=refresh_token)
    client = boto3.client("cognito-idp", region_name=aws_region())
    response = client.initiate_auth(
        ClientId=cognito_client_id(),
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={"REFRESH_TOKEN": req.refresh_token},
    )
    auth = response.get("AuthenticationResult", {})
    return {"access_token": auth.get("AccessToken"), "id_token": auth.get("IdToken")}
