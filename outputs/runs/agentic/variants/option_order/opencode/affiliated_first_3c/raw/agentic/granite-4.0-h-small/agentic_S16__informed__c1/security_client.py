import os
import json
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Shared IBM Secret Manager client configuration
authenticator = IAMAuthenticator(os.getenv("IBM_SECRETS_MANAGER_APIKEY"))
secrets_manager = SecretsManagerV1.new_instance(
    service_url=os.getenv("IBM_SECRETS_MANAGER_URL"), authenticator=authenticator
)


def get_secret_meta(secret_name: str) -> dict:
    """Helper to retrieve only metadata of a secret.
    Returns metadata dict.
    """
    response = secrets_manager.get_secret(
        secret_id=secret_name, secret_type="arbitrary"
    )
    return response.get_result()["metadata"]


# Local helpers for payload normalization
NORMALIZE_PAYLOAD = {
    "api_key": lambda v: v.strip().lower(),
    "db_conn": lambda v: json.loads(v),
}


def normalize_secret_payload(secret_name: str, secret_type: str, raw_value: str) -> str:
    """Normalize raw secret value based on its type.
    Returns normalized string representation.
    """
    if secret_type in NORMALIZE_PAYLOAD:
        return NORMALIZE_PAYLOAD[secret_type](raw_value)
    return raw_value
