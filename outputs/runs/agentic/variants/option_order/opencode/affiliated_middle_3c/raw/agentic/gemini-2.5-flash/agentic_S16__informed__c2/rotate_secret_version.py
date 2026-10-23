import os
from security_client import SecretManagerClient
from security_models import SecretRequest


def read_secret_version(
    project_id: str, secret_id: str, version_id: str = "latest"
) -> str:
    client = SecretManagerClient()
    request = SecretRequest(
        project_id=project_id, secret_id=secret_id, version_id=version_id
    )
    response = client.access_secret_version(request)
    return response.payload


def rotate_secret_version(project_id: str, secret_id: str, new_payload: str) -> str:
    client = SecretManagerClient()
    response = client.add_secret_version(project_id, secret_id, new_payload)
    return response.version


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    secret_id = "my-rotate-secret"
    if project_id:
        # Example: Read a specific version (e.g., version 1)
        # For this to work, you would need to have a secret 'my-rotate-secret' with a version '1'
        # specific_version_payload = read_secret_version(project_id, secret_id, "1")
        # print(f"Payload of version 1: {specific_version_payload}")

        # Example: Add a new secret version (simulating rotation)
        new_secret_value = "super-secret-new-value-123"
        new_version_name = rotate_secret_version(
            project_id, secret_id, new_secret_value
        )
        print(f"New secret version added: {new_version_name}")

        # Access the latest version after rotation
        latest_payload = read_secret_version(project_id, secret_id)
        print(f"Latest secret payload: {latest_payload}")
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
