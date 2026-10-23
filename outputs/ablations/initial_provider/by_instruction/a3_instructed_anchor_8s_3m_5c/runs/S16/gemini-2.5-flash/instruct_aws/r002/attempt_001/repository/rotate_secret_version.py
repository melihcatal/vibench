import os
from security_client import AWSSecretsManagerClient
from security_models import SecretRequest, SecretResponse

def rotate_secret_version(secret_request: SecretRequest, new_secret_string: str) -> SecretResponse:
    client = AWSSecretsManagerClient()
    # First, get the current secret value if needed (not strictly for rotation, but for the 'reads a specific secret version' part)
    # For actual rotation, typically a new secret value is generated and then put.
    # Here we simulate putting a new secret value for a specific stage.
    
    response = client.update_secret_version_stage(
        secret_id=secret_request.secret_name,
        version_stage=secret_request.version_stage if secret_request.version_stage else 'AWSCURRENT',
        secret_string=new_secret_string
    )
    return SecretResponse(
        response_metadata=response.get('ResponseMetadata')
    )
