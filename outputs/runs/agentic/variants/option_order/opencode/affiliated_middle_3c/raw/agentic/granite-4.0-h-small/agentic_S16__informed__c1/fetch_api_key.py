import os
import json
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Local configuration helper (using security_client.py)
from security_client import get_iam_api_key, get_secret_crn

# Authenticate using environment variable set for IBM Cloud
authenticator = IAMAuthenticator(get_iam_api_key())
secrets_manager = SecretsManagerV1(authenticator=authenticator)
secrets_manager.set_service_url(os.getenv("IBM_SECRETS_MANAGER_URL"))


def fetch_api_key():
    """Fetch an API key secret from IBM Cloud Secrets Manager.

    Returns:
        str: The retrieved API key value.
    """
    crn = get_secret_crn("api-key")
    # Retrieve the most recent version of the secret
    response = secrets_manager.get_secret(crn=crn).get_result()
    secret_data = response.get("resources")[0].get("secrets")
    return secret_data  # expected to be the API key string


if __name__ == "__main__":
    api_key = fetch_api_key()
    print(json.dumps({"api_key": api_key}, indent=2))
