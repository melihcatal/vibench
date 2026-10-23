import os
from security_client import get_secrets_manager_client
from security_models import SecretPayload


def get_api_key(secret_name: str) -> SecretPayload | None:
    client = get_secrets_manager_client()
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return SecretPayload(
            name=response.get("Name"),
            value=response.get("SecretString"),
            arn=response.get("ARN"),
        )
    except client.exceptions.ResourceNotFoundException:
        print(f"Secret {secret_name} not found.")
        return None


if __name__ == "__main__":
    api_key_secret_name = os.environ.get("API_KEY_SECRET_NAME")
    if api_key_secret_name:
        api_key_payload = get_api_key(api_key_secret_name)
        if api_key_payload:
            print(f"Successfully fetched API key secret: {api_key_payload.name}")
    else:
        print("API_KEY_SECRET_NAME environment variable not set.")
