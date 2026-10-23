import os
from google.cloud import secretmanager


def rotate_secret_version(project_id: str, secret_id: str, new_secret_data: str) -> str:
    """
    Adds a new secret version to Google Secret Manager, effectively rotating it.
    Provider: Google Cloud Secret Manager
    """
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}/secrets/{secret_id}"
    response = client.add_secret_version(
        request={"parent": parent, "payload": {"data": new_secret_data.encode("UTF-8")}}
    )
    return response.name


def access_specific_secret_version(
    project_id: str, secret_id: str, version_id: str
) -> str:
    """
    Reads a specific secret version or staged value from Google Secret Manager.
    Provider: Google Cloud Secret Manager
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")


if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set)
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # secret_id = "my-rotate-secret"
    # new_data = "new_secret_value_123"
    # new_version_name = rotate_secret_version(project_id, secret_id, new_data)
    # print(f"New secret version created: {new_version_name}")

    # version_to_access = "1" # Or "latest"
    # accessed_data = access_specific_secret_version(project_id, secret_id, version_to_access)
    # print(f"Accessed secret data from version {version_to_access}: {accessed_data}")
    pass
