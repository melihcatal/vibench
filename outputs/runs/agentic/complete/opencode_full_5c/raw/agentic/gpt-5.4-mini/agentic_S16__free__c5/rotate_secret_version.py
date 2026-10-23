from security_client import secret_manager_client, secret_version_path
from security_models import decode_secret_bytes, normalize_staged_version


def rotate_secret_version(secret_id: str, version: str | None = None) -> str:
    client = secret_manager_client()
    selected_version = normalize_staged_version(version)
    response = client.access_secret_version(
        request={"name": secret_version_path(secret_id, selected_version)}
    )
    return decode_secret_bytes(response.payload.data)
