import os
from security_client import get_aws_secrets_manager_client
from security_models import SecretValue


def fetch_api_key(secret_id: str) -> SecretValue:
    client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_id)
    except Exception as e:
        # For a real application, you'd want more specific exception handling.
        print(f"Error fetching secret: {e}")
        raise

    secret_string = get_secret_value_response.get("SecretString")
    secret_binary = get_secret_value_response.get("SecretBinary")

    return SecretValue(
        secret_id=secret_id,
        secret_string=secret_string,
        secret_binary=secret_binary,
        version_id=get_secret_value_response.get("VersionId"),
        version_stages=get_secret_value_response.get("VersionStages"),
    )


if __name__ == "__main__":
    api_key_secret_id = os.environ.get("API_KEY_SECRET_ID", "my/api/key")
    api_key_secret = fetch_api_key(api_key_secret_id)
    if api_key_secret.secret_string:
        print(f"Fetched API Key: {api_key_secret.secret_string[:10]}...")
    elif api_key_secret.secret_binary:
        print("Fetched API Key is binary.")
