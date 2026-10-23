import json
import os
from ibm_secrets_manager_sdk import SecretsManagerV1

client = SecretsManagerV1.new_instance(
    apikey=os.getenv("SECRETS_MANAGER_APIKEY"),
    service_url=os.getenv("SECRETS_MANAGER_SERVICE_URL")
)

def parse_json_secret(secret_name: str) -> dict:
    """Retrieve a secret and parse its JSON payload.
    Args:
        secret_name: Name or ID of the secret holding JSON data.
    Returns:
        Parsed JSON as a Python dict.
    Raises:
        ValueError: If the secret payload is not valid JSON.
    """
    response = client.get_secret(
        secret_type="arbitrary",
        id_or_name=secret_name,
        version_id="latest"
    ).get_result()
    plaintext = response["plaintext"]
    try:
        return json.loads(plaintext)
    except json.JSONDecodeError as exc:
        raise ValueError("Secret payload is not valid JSON") from exc

if __name__ == "__main__":
    # Example: a secret that stores configuration as JSON
    config = parse_json_secret("my-config-secret")
    print("Parsed secret config:", config)