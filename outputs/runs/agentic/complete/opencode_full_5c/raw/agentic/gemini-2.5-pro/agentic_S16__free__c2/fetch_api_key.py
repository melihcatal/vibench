import os
from security_client import get_secret_manager_client


def fetch_api_key(project_id: str, secret_id: str) -> str:
    """
    Fetches an API key from Google Cloud Secret Manager.
    """
    client = get_secret_manager_client()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    try:
        response = client.access_secret_version(request={"name": secret_name})
        api_key = response.payload.data.decode("UTF-8")
        return api_key
    except Exception as e:
        print(f"Error fetching API key: {e}")
        return ""


if __name__ == "__main__":
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    secret = "my-api-key"
    if project:
        key = fetch_api_key(project, secret)
        if key:
            print(f"Successfully fetched API key: {key[:4]}...")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
