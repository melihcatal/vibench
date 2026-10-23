import os
from security_client import SecretManagerHelper
from security_models import SecretPayload

# Google Cloud Project ID can be set as an environment variable
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")


def rotate_secret_version(secret_id: str, version_id: str = "latest") -> SecretPayload:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = SecretManagerHelper(project_id=PROJECT_ID)
    secret_payload = client.get_secret_value(secret_id, version_id)
    return secret_payload


# Example Usage (replace with actual secret_id and set GOOGLE_CLOUD_PROJECT_ID env var)
if __name__ == "__main__":
    try:
        # Fetch the 'latest' version
        latest_secret = rotate_secret_version("my-rotating-secret")
        print(
            f"Fetched latest secret version '{latest_secret.version}': {latest_secret.data.decode('utf-8')[:5]}..."
        )

        # Fetch a specific version (replace '123' with an actual version number)
        # specific_secret = rotate_secret_version("my-rotating-secret", "123")
        # print(f"Fetched specific secret version '{specific_secret.version}': {specific_secret.data.decode('utf-8')[:5]}...")

    except Exception as e:
        print(f"Error fetching secret version: {e}")
