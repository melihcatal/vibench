from ibm_secrets_manager_sdk.secrets_manager_v1 import *
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

def get_specific_secret_version(secret_id: str, version_id: str) -> dict:
    """
    Reads a specific secret version from IBM Cloud Secrets Manager.
    Requires IBM_SECRETS_MANAGER_APIKEY and IBM_SECRETS_MANAGER_SERVICE_URL environment variables.
    """
    api_key = os.environ.get("IBM_SECRETS_MANAGER_APIKEY")
    service_url = os.environ.get("IBM_SECRETS_MANAGER_SERVICE_URL")

    if not api_key or not service_url:
        raise ValueError("IBM_SECRETS_MANAGER_APIKEY and IBM_SECRETS_MANAGER_SERVICE_URL environment variables must be set.")

    authenticator = IAMAuthenticator(api_key)
    service = SecretsManagerV1(authenticator=authenticator)
    service.set_service_url(service_url)

    try:
        secret_data = service.get_secret_version_data(secret_id=secret_id, id=version_id).get_result()
        return secret_data
    except ApiException as e:
        print(f"Error fetching secret version '{version_id}' for secret '{secret_id}': {e.code} - {e.message}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

if __name__ == '__main__':
    # Example usage (requires environment variables for IBM Cloud Secrets Manager)
    # os.environ['IBM_SECRETS_MANAGER_APIKEY'] = 'YOUR_IBM_SECRETS_MANAGER_APIKEY'
    # os.environ['IBM_SECRETS_MANAGER_SERVICE_URL'] = 'https://<region>.secrets-manager.appdomain.cloud'
    # os.environ['SECRET_TO_ROTATE_ID'] = 'your_secret_uuid'
    # os.environ['SECRET_VERSION_ID'] = 'your_version_uuid'
    secret_to_rotate_id = os.environ.get('SECRET_TO_ROTATE_ID', 'your_secret_id')
    secret_version_id = os.environ.get('SECRET_VERSION_ID', 'your_secret_version_id')
    try:
        version_data = get_specific_secret_version(secret_to_rotate_id, secret_version_id)
        print(f"Successfully retrieved secret version data: {version_data}")
    except Exception:
        print("Failed to retrieve specific secret version.")
