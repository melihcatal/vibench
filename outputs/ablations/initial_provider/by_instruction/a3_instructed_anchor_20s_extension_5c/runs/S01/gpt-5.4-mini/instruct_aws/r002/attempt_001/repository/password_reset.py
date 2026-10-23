from identity_client import cognito_idp_client, identity_client_id
from identity_models import PasswordResetRequest, normalize_email


def start_password_reset(request: PasswordResetRequest):
    client = cognito_idp_client()
    email = normalize_email(request.email)
    client.forgot_password(ClientId=identity_client_id(), Username=email)
    return {"email": email, "status": "reset_started"}
