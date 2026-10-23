import os

from identity_client import cognito_idp_client, config, prepare_identity_payload


def register_user(email: str, password: str):
    payload = prepare_identity_payload(email, password)
    client = cognito_idp_client()
    cfg = config()
    return client.sign_up(
        ClientId=cfg["client_id"],
        Username=payload["email"],
        Password=payload["password"],
        UserAttributes=[{"Name": "email", "Value": payload["email"]}],
    )
