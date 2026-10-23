import os
from ibm_secrets_manager_sdk import SecretsManagerV1

# Initialize the SDK client using environment variables for credentials
client = SecretsManagerV1.new_instance(
    apikey=os.getenv("SECRETS_MANAGER_APIKEY"),
    service_url=os.getenv("SECRETS_MANAGER_SERVICE_URL")
)

def get_secret(secret_name: str, version_id: str = "latest") -> dict:
    """Generic helper to retrieve a secret from IBM Cloud Secrets Manager.
    Args:
        secret_name: Name or ID of the secret.
        version_id: Specific version to fetch; defaults to latest.
    Returns:
        The raw response from the API (including plaintext).
    """
    return client.get_secret(
        secret_type="arbitrary",
        id_or_name=secret_name,
        version_id=version_id
    ).get_result()

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     resp = get_secret("my-example-secret")
#     print("Secret payload:", resp["plaintext"])