import os
from ibm_secrets_manager_sdk import SecretsManagerV1

# Initialize SDK client using environment variable for API key
client = SecretsManagerV1.new_instance(
    apikey=os.getenv("SECRETS_MANAGER_APIKEY"),
    service_url=os.getenv("SECRETS_MANAGER_SERVICE_URL")
)

def fetch_api_key(secret_name: str) -> str:
    """Retrieve the API key stored in the IBM Cloud Secrets Manager.
    Args:
        secret_name: Name or ID of the secret containing the API key.
    Returns:
        The secret value as a string.
    Raises:
        Exception if the secret cannot be retrieved.
    """
    response = client.get_secret(
        secret_type="arbitrary",
        id_or_name=secret_name,
        version_id="latest"
    ).get_result()
    return response["plaintext"]

if __name__ == "__main__":
    # Example usage – replace with your secret name
    api_key = fetch_api_key("my-api-key-secret")
    print("Fetched API key:", api_key)