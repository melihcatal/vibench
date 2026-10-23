import os

from identity_client import CognitoClient
from identity_models import RefreshSessionRequest

def refresh_session(payload: RefreshSessionRequest, config: Optional[Dict[str, Any]] = None):
    config = config or {}
    region = config.get("region", os.environ.get("AWS_REGION"))
    client_id = config.get("client_id", os.environ.get("COGNITO_CLIENT_ID"))
    client_secret = config.get("client_secret", os.environ.get("COGNITO_CLIENT_SECRET")) # Not strictly needed for refresh in many cases, but kept for consistency

    if not all([region, client_id]):
        raise ValueError("AWS region and Cognito client ID must be provided in config or environment variables.")

    cognito_client = CognitoClient(region=region, client_id=client_id, client_secret=client_secret)
    
    response = cognito_client.refresh_token(payload.refresh_token)
    return response
