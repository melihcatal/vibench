import os
import json

# Provider-specific configuration
# Using IBM Cloud Secrets Manager
IBMCLOUD_APIKEY = os.getenv("IBMCLOUD_SECRETS_MANAGER_APIKEY")
IBMCLOUD_ENDPOINT = os.getenv(
    "IBMCLOUD_SECRETS_MANAGER_ENDPOINT", "https://secrets-manager.cloud.ibm.com"
)

from ibm_secrets_manager_sdk.secrets_manager_v1 import SecretsManagerV1
from ibm_secrets_manager_sdk.auth import IAMAuthenticator

authenticator = IAMAuthenticator(IBMCLOUD_APIKEY)
client = SecretsManagerV1(authenticator=authenticator)
client.set_service_url(IBMCLOUD_ENDPOINT)


def fetch_api_key(secret_name: str) -> str:
    """Fetch an API key secret from IBM Cloud Secrets Manager.
    Returns the secret payload as a string.
    """
    response = client.get_secret(secret_id=secret_name, version_id="latest")
    payload = response.get_result()
    # Assume the secret payload is stored under "api_key"
    return payload.get("api_key", "")


if __name__ == "__main__":
    # Example usage
    secret_name = os.getenv("API_KEY_SECRET_NAME")
    if secret_name:
        print("Fetched API key:", fetch_api_key(secret_name))
    else:
        print("Set API_KEY_SECRET_NAME env var")
