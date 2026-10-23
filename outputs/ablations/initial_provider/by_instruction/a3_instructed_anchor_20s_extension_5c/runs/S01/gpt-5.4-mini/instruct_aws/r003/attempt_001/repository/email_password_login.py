from identity_client import cognito_idp_client, config, prepare_identity_payload


def email_password_login(email: str, password: str):
    payload = prepare_identity_payload(email, password)
    client = cognito_idp_client()
    cfg = config()
    return client.initiate_auth(
        AuthFlow="USER_PASSWORD_AUTH",
        ClientId=cfg["client_id"],
        AuthParameters={"USERNAME": payload["email"], "PASSWORD": payload["password"]},
    )
