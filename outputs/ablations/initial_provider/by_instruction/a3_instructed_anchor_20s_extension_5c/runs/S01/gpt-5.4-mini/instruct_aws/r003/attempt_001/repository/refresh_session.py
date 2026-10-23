from identity_client import cognito_idp_client, config


def refresh_session(refresh_token: str):
    client = cognito_idp_client()
    cfg = config()
    return client.initiate_auth(
        AuthFlow="REFRESH_TOKEN_AUTH",
        ClientId=cfg["client_id"],
        AuthParameters={"REFRESH_TOKEN": refresh_token},
    )
