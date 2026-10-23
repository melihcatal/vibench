import os
from ibm_secrets_manager_sdk import SecretsManagerV1

client = SecretsManagerV1.new_instance(
    apikey=os.getenv("SECRETS_MANAGER_APIKEY"),
    service_url=os.getenv("SECRETS_MANAGER_SERVICE_URL")
)

def rotate_secret_version(secret_name: str, version_id: str) -> dict:
    """Read a specific version/staged value of a secret.
    Args:
        secret_name: Name or ID of the secret.
        version_id: The version identifier to retrieve.
    Returns:
        The secret payload for the requested version.
    Raises:
        Exception: If the version cannot be fetched.
    """
    resp = client.get_secret(
        secret_type="arbitrary",
        id_or_name=secret_name,
        version_id=version_id
    ).get_result()
    return resp["plaintext"]

if __name__ == "__main__":
    # Example: fetch a staged version named 'staged-1'
    payload = rotate_secret_version("my-secret", "staged-1")
    print("Rotated secret payload:", payload)