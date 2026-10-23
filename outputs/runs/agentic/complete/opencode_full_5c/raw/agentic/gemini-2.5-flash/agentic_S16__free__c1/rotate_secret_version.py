import os
from security_client import SecretManagementClient


def rotate_secret_version(secret_id: str, new_secret_payload: str) -> str:
    client = SecretManagementClient()

    # 1. Read the current latest version (or a specific staged value if needed)
    print(f"Reading latest version of secret {secret_id}...")
    current_payload = client.get_secret_payload(
        secret_id=secret_id, version_id="latest"
    )
    if current_payload:
        print(
            f"Current secret (latest): {current_payload.data.decode('utf-8')[:10]}..."
        )
    else:
        print(f"No current secret found for {secret_id}.")

    # 2. Add a new secret version
    print(f"Adding new version to secret {secret_id}...")
    new_version = client.add_secret_version(
        secret_id=secret_id, payload=new_secret_payload.encode("utf-8")
    )
    print(f"New secret version created: {new_version.name}")

    # In a real rotation, you would typically disable the old version or mark it for destruction
    # For this example, we just add a new version.
    return new_version.name


if __name__ == "__main__":
    # Example usage: Replace 'your-secret-to-rotate-id' with your actual secret ID
    # And ensure GOOGLE_CLOUD_PROJECT environment variable is set
    try:
        # For demonstration, we're just providing a simple new secret string.
        # In a real scenario, this would be a newly generated secret.
        rotated_version_name = rotate_secret_version(
            "your-secret-to-rotate-id", "new_secret_value_" + os.urandom(4).hex()
        )
        print(f"Secret rotation simulated. New active version: {rotated_version_name}")
    except Exception as e:
        print(f"An error occurred during secret rotation: {e}")
