import os

from identity_client import CognitoClient
from identity_models import PasswordResetRequest

def password_reset(payload: PasswordResetRequest, config: Optional[Dict[str, Any]] = None):
    config = config or {}
    region = config.get("region", os.environ.get("AWS_REGION"))
    client_id = config.get("client_id", os.environ.get("COGNITO_CLIENT_ID"))
    client_secret = config.get("client_secret", os.environ.get("COGNITO_CLIENT_SECRET"))

    if not all([region, client_id]):
        raise ValueError("AWS region and Cognito client ID must be provided in config or environment variables.")

    cognito_client = CognitoClient(region=region, client_id=client_id, client_secret=client_secret)
    
    response = cognito_client.forgot_password(payload.email)
    return response
