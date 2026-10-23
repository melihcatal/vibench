import os
from security_client import AWSSecretsManagerClient
from security_models import SecretRequest, SecretResponse

def fetch_api_key(secret_request: SecretRequest) -> SecretResponse:
    client = AWSSecretsManagerClient()
    response = client.get_secret(secret_request.secret_name)
    return SecretResponse(
        secret_string=response.get('SecretString'),
        secret_binary=response.get('SecretBinary'),
        response_metadata=response.get('ResponseMetadata')
    )
