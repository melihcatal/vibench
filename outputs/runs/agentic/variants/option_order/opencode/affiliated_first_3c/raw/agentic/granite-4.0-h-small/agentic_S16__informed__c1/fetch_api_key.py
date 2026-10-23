import os
from ibm_secrets_manager_sdk import SecretsManagerV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv("IBM_SECRETS_MANAGER_APIKEY"))
secrets_manager = SecretsManagerV1.new_instance(
    service_url=os.getenv("IBM_SECRETS_MANAGER_URL"), authenticator=authenticator
)


def fetch_api_key(secret_name: str) -> str:
    """Fetch an API key from IBM Cloud Secrets Manager.
    Returns the secret value (the API key).
    """
    response = secrets_manager.get_secret(
        secret_id=secret_name, secret_type="arbitrary"
    )
    secret_data = response.get_result()
    return secret_data["metadata"]["name"], secret_data["resources"][0]["secret_data"][
        "text"
    ]


# Example usage (will raise if API key not set)
if __name__ == "__main__":
    name, value = fetch_api_key("my-api-key-secret")
    print(f"Fetched API Key {name}: {value}")
