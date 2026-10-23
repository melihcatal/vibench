import os
from datetime import datetime
from security_client import SecretManagementClient


def summarize_secret_rotation_status(secret_id: str):
    client = SecretManagementClient()

    print(f"--- Rotation Summary for Secret: {secret_id} ---")

    # Get secret metadata
    secret_metadata = client.get_secret_metadata(secret_id)
    if secret_metadata:
        print(f"Secret Name: {secret_metadata.name}")
        print(f"Labels: {secret_metadata.labels}")
        if secret_metadata.create_time:
            print(f"Created At: {secret_metadata.create_time.isoformat()}")
    else:
        print(f"Secret {secret_id} not found.")
        return

    # List all secret versions
    versions = client.list_secret_versions(secret_id=secret_id)

    if not versions:
        print("No versions found for this secret.")
        return

    print("\nVersions Status:")
    active_versions = 0
    for version in sorted(versions, key=lambda v: v.create_time, reverse=True):
        create_time_str = (
            version.create_time.isoformat() if version.create_time else "N/A"
        )
        print(
            f"  Version: {version.name.split('/')[-1]}, State: {version.state}, Created: {create_time_str}"
        )
        if version.state == secretmanager.SecretVersion.State.ENABLED:
            active_versions += 1

    print(f"\nTotal versions: {len(versions)}")
    print(f"Active versions: {active_versions}")
    print("------------------------------------------")


if __name__ == "__main__":
    # Example usage: Replace 'your-secret-id' with an actual secret ID
    # And ensure GOOGLE_CLOUD_PROJECT environment variable is set
    try:
        summarize_secret_rotation_status("your-secret-to-rotate-id")
    except Exception as e:
        print(f"An error occurred while summarizing rotation status: {e}")
