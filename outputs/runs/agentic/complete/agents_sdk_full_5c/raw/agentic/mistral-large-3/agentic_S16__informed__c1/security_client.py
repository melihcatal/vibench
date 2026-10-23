from typing import Optional, Dict, Any
import os
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_secrets_manager_sdk import SecretsManagerV1

class IBMSecretsManagerClient:
    def __init__(self):
        api_key = os.getenv("IBM_SECRETS_MANAGER_APIKEY")
        service_url = os.getenv("IBM_SECRETS_MANAGER_URL")
        if not api_key or not service_url:
            raise ValueError("IBM Secrets Manager credentials not configured")
        
        authenticator = IAMAuthenticator(api_key)
        self.client = SecretsManagerV1(authenticator=authenticator)
        self.client.set_service_url(service_url)

    def get_secret(self, request: Dict[str, Any]) -> Dict[str, Any]:
        secret_type = request.get("type", "arbitrary")
        secret_id = request["name"]
        
        if secret_type == "arbitrary":
            response = self.client.get_secret(
                secret_type=secret_type,
                id=secret_id
            )
            return {
                "value": response.get_result()["resources"][0]["secret_data"]["payload"],
                "version": response.get_result()["resources"][0]["version_id"]
            }
        else:
            raise ValueError(f"Unsupported secret type: {secret_type}")

def get_secrets_manager_client():
    return IBMSecretsManagerClient()