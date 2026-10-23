from security_client import get_secret_manager_client
from google.api_core.exceptions import NotFound

def fetch_api_key(project_id: str, secret_id: str) -> str | None:
    """
    Fetches an API key from Google Secret Manager.
    Assumes the latest version is desired.
    """
    client = get_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    try:
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except NotFound:
        print(f"Secret {secret_id} not found in project {project_id}.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
