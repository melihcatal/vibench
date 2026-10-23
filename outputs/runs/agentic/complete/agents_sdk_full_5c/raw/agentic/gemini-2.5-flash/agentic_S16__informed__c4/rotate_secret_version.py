from security_client import get_secret_manager_client
from google.api_core.exceptions import NotFound

def read_secret_version(project_id: str, secret_id: str, version_id: str) -> str | None:
    """
    Reads a specific secret version from Google Secret Manager.
    version_id can be 'latest', '1', '2', etc. or a specific alias.
    """
    client = get_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except NotFound:
        print(f"Secret version {version_id} for secret {secret_id} not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def list_secret_versions(project_id: str, secret_id: str):
    """
    Lists secret versions for a given secret.
    """
    client = get_secret_manager_client()
    parent = f"projects/{project_id}/secrets/{secret_id}"
    versions = client.list_secret_versions(request={"parent": parent})
    return [
        {
            "name": version.name,
            "state": version.state.name,
            "create_time": version.create_time.isoformat() if version.create_time else None,
        }
        for version in versions
    ]
