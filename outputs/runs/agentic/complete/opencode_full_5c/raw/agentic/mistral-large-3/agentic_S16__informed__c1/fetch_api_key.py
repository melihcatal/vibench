from typing import Optional
import os
import json
from ibm_secrets_manager_sdk import SecretsManagerV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def fetch_api_key(secret_name: str) -> Optional[str]:
    """
    Fetches an API key from IBM Cloud Secrets Manager.
    """
    api_key = os.getenv("IBM_SECRETS_MANAGER_APIKEY")
    service_url = os.getenv("IBM_SECRETS_MANAGER_URL")

    if not api_key or not service_url:
        raise ValueError("IBM Cloud Secrets Manager credentials not configured.")

    authenticator = IAMAuthenticator(api_key)
    secrets_manager = SecretsManagerV2(authenticator=authenticator)
    secrets_manager.set_service_url(service_url)

    try:
        secret = secrets_manager.get_secret(
            secret_type="arbitrary", id=secret_name
        ).get_result()

        return secret.get("resources", [{}])[0].get("secret_data", {}).get("payload")
    except Exception as e:
        print(f"Failed to fetch API key: {e}")
        return None
