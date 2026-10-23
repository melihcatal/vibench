import os
from ibm_secrets_manager_sdk import SecretsManagerV1

# Create SDK client with credentials from environment
client = SecretsManagerV1.new_instance(
    apikey=os.getenv("SECRETS_MANAGER_APIKEY"),
    service_url=os.getenv("SECRETS_MANAGER_SERVICE_URL")
)

def fetch_db_secret(secret_name: str) -> str:
    """Fetch a database connection secret from Secrets Manager.
    Args:
        secret_name: Name or ID of the secret that stores DB credentials.
    Returns:
        Plaintext secret data (often JSON/dict-like).
    Raises:
        Exception: If the secret cannot be retrieved.
    """
    resp = client.get_secret(
        secret_type="arbitrary",
        id_or_name=secret_name,
        version_id="latest"
    ).get_result()
    return resp["plaintext"]

if __name__ == "__main__":
    secret_data = fetch_db_secret("my-db-secret")
    print("Database secret payload:", secret_data)