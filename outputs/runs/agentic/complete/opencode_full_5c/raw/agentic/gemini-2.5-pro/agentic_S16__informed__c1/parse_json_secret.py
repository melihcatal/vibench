import os
import json
from security_client import get_secrets_manager_client
from security_models import Secret


def get_json_secret(secret_name: str) -> Secret:
    """
    Retrieves and parses a JSON-formatted secret from AWS Secrets Manager.
    """
    client = get_secrets_manager_client()
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_value = json.loads(response["SecretString"])
        secret_version = response.get("VersionId")
        return Secret(name=secret_name, value=secret_value, version=secret_version)
    except Exception as e:
        print(f"Failed to retrieve or parse JSON secret '{secret_name}': {e}")
        return None


if __name__ == "__main__":
    json_secret_id = os.environ.get("JSON_SECRET_NAME")
    if json_secret_id:
        parsed_secret = get_json_secret(json_secret_id)
        if parsed_secret:
            print(
                f"Successfully parsed secret '{parsed_secret.name}' (Version: {parsed_secret.version})"
            )
            # print("Secret Content:", parsed_secret.value)
    else:
        print("Environment variable JSON_SECRET_NAME not set.")
