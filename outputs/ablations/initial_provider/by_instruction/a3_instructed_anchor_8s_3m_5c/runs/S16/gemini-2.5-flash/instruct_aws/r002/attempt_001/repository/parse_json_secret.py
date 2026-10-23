import os
import json
from typing import Dict, Any
from security_client import AWSSecretsManagerClient
from security_models import SecretRequest

def parse_json_secret(secret_request: SecretRequest) -> Dict[str, Any]:
    client = AWSSecretsManagerClient()
    response = client.get_secret(secret_request.secret_name)
    secret_string = response.get('SecretString')
    if secret_string:
        return json.loads(secret_string)
    raise ValueError("Secret does not contain a JSON string.")
