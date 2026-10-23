from identity_client import add_secret_hash, create_cognito_client, prepare_username


def refresh_session(payload, config=None):
    client, cfg = create_cognito_client(config)
    username = prepare_username(payload)
    request = {"AuthFlow": "REFRESH_TOKEN_AUTH", "ClientId": cfg["client_id"], "AuthParameters": {"REFRESH_TOKEN": payload["refresh_token"], "USERNAME": username}}
    add_secret_hash(request["AuthParameters"], cfg, username)
    response = client.initiate_auth(**request)
    auth = response["AuthenticationResult"]
    return {"access_token": auth.get("AccessToken"), "id_token": auth.get("IdToken"), "refresh_token": auth.get("RefreshToken", payload["refresh_token"]), "expires_in": auth.get("ExpiresIn")}
