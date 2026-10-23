import os
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv("IBM_SECRETS_MANAGER_APIKEY"))
secrets_manager = SecretsManagerV1.new_instance(
    service_url=os.getenv("IBM_SECRETS_MANAGER_URL"), authenticator=authenticator
)


def rotate_secret_version(secret_name: str, version: str) -> dict:
    """Read a specific version (or staged value) of a secret from IBM Cloud Secrets Manager.
    Returns the response containing the requested version data.
    """
    response = secrets_manager.get_secret_version(
        secret_id=secret_name, version_id=version
    )
    return response.get_result()


# Example usage
if __name__ == "__main__":
    result = rotate_secret_version("my-secret", "1")
    print("Version info:", result["resources"][0])
