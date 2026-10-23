# fetch_api_key.py
# [SAME-SCENARIO]
# Fetches an API key from IBM Cloud Secrets Manager

import os
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_secrets_manager_sdk.exceptions import ApiException


def fetch_api_key(secret_name: str) -> str:
    """Retrieve an API key secret from IBM Cloud Secrets Manager.

    Args:
        secret_name: Name of the secret containing the API key.

    Returns:
        The API key value as a string.
    """
    api_key = os.getenv("IBM_SECRETS_MANAGER_APIKEY")
    if not api_key:
        raise RuntimeError("Set IBM_SECRETS_MANAGER_APIKEY environment variable")

    client = SecretsManagerV1.new_instance(authenticator="iam", apikey=api_key)
    client.service_url = (
        "https://secrets-manager.test.cloud.ibm.com"  # Adjust as needed
    )

    secret_data = client.get_secret(
        secret_type="arbitrary", secret_name=secret_name, version_id="latest"
    ).get_result()

    return secret_data["plaintext"]
