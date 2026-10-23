from identity_client import cognito_idp_client, load_identity_config
from identity_models import PasswordResetRequest, normalize_email, to_payload


def password_reset(email: str):
    config = load_identity_config()
    client = cognito_idp_client()
    payload = to_payload(PasswordResetRequest(email=normalize_email(email)))
    return client.forgot_password(ClientId=config.client_id, Username=payload["email"])
