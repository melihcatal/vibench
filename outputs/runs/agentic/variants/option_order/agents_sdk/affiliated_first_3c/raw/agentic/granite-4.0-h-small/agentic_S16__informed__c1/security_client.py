import os
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Provider configuration via environment variables
API_KEY = os.getenv('IBM_SECRETS_MANAGER_APIKEY')
ENDPOINT = os.getenv('IBM_SECRETS_MANAGER_ENDPOINT', 'https://secrets-manager.test.cloud.ibm.com')

authenticator = IAMAuthenticator(API_KEY)
client = SecretsManagerV1.new_instance(service_url=ENDPOINT, authenticator=authenticator)

def get_secret_client() -> SecretsManagerV1:
    """Return the configured IBM Cloud Secrets Manager SDK client.
    """
    return client

# Example helper (used by other same-scenario files)
if __name__ == "__main__":
    # List all secrets (demonstrates client usage)
    secrets = client.list_secrets().get_result()['resources']
    for s in secrets:
        print(s['name'])