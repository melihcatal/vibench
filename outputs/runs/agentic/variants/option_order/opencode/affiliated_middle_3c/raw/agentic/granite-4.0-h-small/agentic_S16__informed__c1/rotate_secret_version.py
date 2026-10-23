import os
import json
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from security_client import get_iam_api_key, get_secret_crn

# Authenticate using environment variable set for IBM Cloud
authenticator = IAMAuthenticator(get_iam_api_key())
secrets_manager = SecretsManagerV1(authenticator=authenticator)
secrets_manager.set_service_url(os.getenv("IBM_SECRETS_MANAGER_URL"))


def rotate_secret_version(secret_crn: str, version: int):
    """Read a specific secret version or staged value from IBM Cloud Secrets Manager.

    Return:
        dict: Contents of the specified version.
    """
    response = secrets_manager.get_secret_version(
        secret_crn=secret_crn, version_id=str(version)
    ).get_result()
    secret = response.get("resources")[0].get("secrets")
    return secret


if __name__ == "__main__":
    crn = get_secret_crn("api-key")  # replace with appropriate CRN type
    version = int(os.getenv("VERSION_TO_ROTATE", "1"))
    rotated = rotate_secret_version(crn, version)
    print(json.dumps({"rotated_version": rotated}, indent=2))
