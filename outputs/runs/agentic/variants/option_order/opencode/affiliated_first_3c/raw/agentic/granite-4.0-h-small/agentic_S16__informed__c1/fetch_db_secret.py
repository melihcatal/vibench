import os
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv("IBM_SECRETS_MANAGER_APIKEY"))
secrets_manager = SecretsManagerV1.new_instance(
    service_url=os.getenv("IBM_SECRETS_MANAGER_URL"), authenticator=authenticator
)


def fetch_db_secret(secret_name: str) -> dict:
    """Retrieve a database connection secret from IBM Cloud Secrets Manager.
    Returns a dict with secret metadata and the secret value.
    """
    response = secrets_manager.get_secret(
        secret_id=secret_name, secret_type="arbitrary"
    )
    return response.get_result()


# Example usage
if __name__ == "__main__":
    secret = fetch_db_secret("my-db-conn-secret")
    print("Fetched secret metadata:", secret["metadata"])
    print("Secret value:", secret["resources"][0]["secret_data"])
