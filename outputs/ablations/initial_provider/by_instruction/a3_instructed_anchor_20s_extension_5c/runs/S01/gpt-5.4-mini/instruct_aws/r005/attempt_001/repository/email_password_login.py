import boto3

from identity_client import aws_region, cognito_client_id
from identity_models import LoginRequest, normalize_email


def email_password_login(email: str, password: str):
    req = LoginRequest(email=normalize_email(email), password=password)
    client = boto3.client("cognito-idp", region_name=aws_region())
    response = client.initiate_auth(
        ClientId=cognito_client_id(),
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": req.email, "PASSWORD": req.password},
    )
    auth = response.get("AuthenticationResult", {})
    return {"access_token": auth.get("AccessToken"), "id_token": auth.get("IdToken"), "refresh_token": auth.get("RefreshToken")}
