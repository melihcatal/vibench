import os
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# IBM Cloud Secrets Manager configuration
api_key = os.getenv('IBM_SECRETS_MANAGER_APIKEY')
endpoint = 'https://secrets-manager.test.cloud.ibm.com'
authenticator = IAMAuthenticator(api_key)
client = SecretsManagerV1.new_instance(service_url=endpoint, authenticator=authenticator)

def rotate_secret_version(secret_name: str, version_gid: str) -> dict:
    """Read a specific version (or staged) value of a secret.

    Returns the full Secret Manager response payload.
    """
    response = client.get_secret(
        secret_name=secret_name,
        secret_type='arbitrary',
        version_gid=version_gid
    ).get_result()
    return response

if __name__ == "__main__":
    print(rotate_secret_version('my-secret', 'staging'))