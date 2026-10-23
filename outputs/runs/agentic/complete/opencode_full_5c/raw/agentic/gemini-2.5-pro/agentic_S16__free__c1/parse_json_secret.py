import os
import json
from security_client import get_azure_key_vault_client
from security_models import SecretValue


def parse_json_secret(secret_name: str) -> dict:
    client = get_azure_key_vault_client()
    try:
        retrieved_secret = client.get_secret(secret_name)
    except Exception as e:
        print(f"Error fetching secret: {e}")
        raise

    secret_value = retrieved_secret.value

    try:
        parsed_json = json.loads(secret_value)
    except json.JSONDecodeError as e:
        print(f"Secret value for '{secret_name}' is not valid JSON. Error: {e}")
        raise

    return parsed_json


if __name__ == "__main__":
    json_secret_name = os.environ.get("JSON_SECRET_NAME", "my-json-secret")
    try:
        secret_data = parse_json_secret(json_secret_name)
        print(f"Successfully parsed JSON secret. Keys: {list(secret_data.keys())}")
    except ValueError:
        print(
            "Could not fetch or parse secret. Check logs and environment variables (AZURE_VAULT_URL)."
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
