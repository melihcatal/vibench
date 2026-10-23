import os
import json
from security_client import get_secrets_manager_client


def get_and_parse_json_secret(secret_name: str) -> dict | None:
    client = get_secrets_manager_client()
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response.get("SecretString")
        if secret_string:
            return json.loads(secret_string)
        return None
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret {secret_name} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Failed to parse JSON from secret {secret_name}.")
        return None


if __name__ == "__main__":
    json_secret_name = os.environ.get("JSON_SECRET_NAME")
    if json_secret_name:
        parsed_secret = get_and_parse_json_secret(json_secret_name)
        if parsed_secret:
            print(f"Successfully parsed secret: {parsed_secret}")
    else:
        print("JSON_SECRET_NAME environment variable not set.")
