from identity_client import cognito_idp_client, config, prepare_identity_payload


def password_reset(email: str):
    payload = prepare_identity_payload(email, "unused")
    client = cognito_idp_client()
    cfg = config()
    return client.forgot_password(ClientId=cfg["client_id"], Username=payload["email"])
