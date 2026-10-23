import os
import json
from security_client import get_secrets_manager_client


def get_and_parse_json_secret(secret_id: str) -> dict:
    """
    Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.
    """
    client = get_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_id)
        secret = get_secret_value_response["SecretString"]
        return json.loads(secret)
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret '{secret_id}' not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Could not decode JSON from secret '{secret_id}'.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}


if __name__ == "__main__":
    json_secret_id = os.environ.get("JSON_SECRET_ID", "my-app/json-config")
    config = get_and_parse_json_secret(json_secret_id)
    if config:
        print(f"Successfully parsed secret: {json_secret_id}")
        # print(f"Content: {config}")
    else:
        print(f"Could not parse secret: {json_secret_id}")
