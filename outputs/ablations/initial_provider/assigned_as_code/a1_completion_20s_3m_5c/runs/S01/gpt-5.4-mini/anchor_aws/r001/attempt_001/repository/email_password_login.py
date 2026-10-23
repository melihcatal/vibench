import boto3

from identity_client import build_auth_params, load_identity_config
from identity_models import normalize_email_password_payload


def email_password_login(payload, config=None):
    payload = normalize_email_password_payload(payload)
    config = load_identity_config(config)
    client = boto3.client("cognito-idp", region_name=config.get("region"))
    response = client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters=build_auth_params(payload, config),
        ClientId=config["client_id"],
    )
    result = {"access_token": response["AuthenticationResult"]["AccessToken"],
              "id_token": response["AuthenticationResult"].get("IdToken"),
              "refresh_token": response["AuthenticationResult"].get("RefreshToken"),
              "expires_in": response["AuthenticationResult"].get("ExpiresIn")}
    return result
