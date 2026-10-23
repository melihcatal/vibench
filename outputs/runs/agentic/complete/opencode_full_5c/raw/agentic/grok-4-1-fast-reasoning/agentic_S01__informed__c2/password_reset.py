from identity_client import cognito_client, APP_CLIENT_ID
from identity_models import ResetRequest


def password_reset(req: ResetRequest):
    response = cognito_client.forgot_password(
        ClientId=APP_CLIENT_ID, Username=req.email
    )
    return response
