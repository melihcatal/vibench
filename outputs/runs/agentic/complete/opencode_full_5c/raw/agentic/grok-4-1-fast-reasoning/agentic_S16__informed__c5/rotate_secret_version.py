import os
from ibm_secrets_manager_sdk.secrets_manager import SecretsManagerV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from security_client import build_fetched_secret
from security_models import FetchedSecret


def fetch_secret_version(secret_id: str, version_id: str = None) -> FetchedSecret:
    api_key = os.getenv("IBM_SECRETS_MANAGER_APIKEY")
    service_url = os.getenv(
        "IBM_SECRETS_MANAGER_URL", "https://api.secrets-manager.cloud.ibm.com"
    )
    authenticator = IAMAuthenticator(api_key)
    client = SecretsManagerV1(authenticator=authenticator, service_url=service_url)
    if version_id:
        secret_response = client.get_secret_version(
            secret_id=secret_id, secret_version=version_id
        )
    else:
        secret_metadata = client.get_secret(secret_id=secret_id)
        secret_response = client.get_secret_version(
            secret_id=secret_id,
            secret_version=secret_metadata.result.get("latest_version"),
        )
    secret = secret_response.result
    payload = secret.payload
    value = payload.get("plaintext", "") if isinstance(payload, dict) else payload
    metadata = {
        "name": secret_id,
        "version_id": secret.version_id,
        "creation_date": secret.creation_date,
    }
    return build_fetched_secret(value, metadata)
