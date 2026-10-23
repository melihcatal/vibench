import os
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Configure using environment variable or set directly
api_key = os.getenv('IBM_SECRETS_MANAGER_APIKEY')
endpoint = 'https://secrets-manager.test.cloud.ibm.com'

authenticator = IAMAuthenticator(api_key)
client = SecretsManagerV1.new_instance(service_url=endpoint, authenticator=authenticator)

def fetch_api_key(secret_name: str) -> str:
    """Retrieve the value of an API key stored as a secret.
    Returns the plain text value of the secret.
    """
    response = client.get_secret(
        secret_name=secret_name,
        secret_type='arbitrary',
        version_gid='latest'
    ).get_result()
    return response['plaintext']

if __name__ == "__main__":
    print(fetch_api_key('my-api-key'))