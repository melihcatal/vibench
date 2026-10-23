from security_client import get_client, build_secret_path
from security_models import SecretResponse


def rotate_secret_version(secret_name: str, version: str) -> dict:
    client = get_client()
    name = build_secret_path(secret_name, version)
    response = client.access_secret_version(name=name)
    payload = SecretResponse.from_google_secret_manager(response)
    return {"name": name, "length": len(payload.as_text()), "version": version}
