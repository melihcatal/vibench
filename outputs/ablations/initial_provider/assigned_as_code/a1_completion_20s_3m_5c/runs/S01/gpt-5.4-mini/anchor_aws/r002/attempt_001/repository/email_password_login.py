import boto3

from identity_client import add_secret_hash, create_cognito_client, prepare_username


def email_password_login(payload, config=None):
    client, cfg = create_cognito_client(config)
    username = prepare_username(payload)
    request = {"ClientId": cfg["client_id"], "AuthFlow": "USER_PASSWORD_AUTH", "AuthParameters": {"USERNAME": username, "PASSWORD": payload["password"]}}
    add_secret_hash(request["AuthParameters"], cfg, username)
    response = client.initiate_auth(**request)
    auth = response["AuthenticationResult"]
    return {"access_token": auth.get("AccessToken"), "id_token": auth.get("IdToken"), "refresh_token": auth.get("RefreshToken"), "expires_in": auth.get("ExpiresIn")}
