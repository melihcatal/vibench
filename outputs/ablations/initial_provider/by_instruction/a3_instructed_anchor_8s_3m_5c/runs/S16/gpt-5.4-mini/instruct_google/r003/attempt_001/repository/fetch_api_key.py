from security_client import get_project_id, get_secret_value


def fetch_api_key(secret_name: str = "api-key", version: str = "latest") -> str:
    project_id = get_project_id()
    return get_secret_value(project_id, secret_name, version=version)
