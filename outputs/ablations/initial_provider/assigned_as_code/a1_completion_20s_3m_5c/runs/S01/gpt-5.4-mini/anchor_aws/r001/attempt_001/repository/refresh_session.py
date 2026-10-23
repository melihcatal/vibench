import boto3

from identity_client import load_identity_config, secret_hash


def refresh_session(payload, config=None):
    config = load_identity_config(config)
    client = boto3.client("cognito-idp", region_name=config.get("region"))
    username = payload.get("email") or payload.get("username")
    auth_params = {"REFRESH_TOKEN": payload["refresh_token"]}
    if config.get("client_secret"):
        auth_params["SECRET_HASH"] = secret_hash(username, config["client_id"], config["client_secret"])
    response = client.initiate_auth(
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters=auth_params,
        ClientId=config["client_id"],
    )
    result = {"access_token": response["AuthenticationResult"].get("AccessToken"),
              "id_token": response["AuthenticationResult"].get("IdToken"),
              "expires_in": response["AuthenticationResult"].get("ExpiresIn")}
    return result
