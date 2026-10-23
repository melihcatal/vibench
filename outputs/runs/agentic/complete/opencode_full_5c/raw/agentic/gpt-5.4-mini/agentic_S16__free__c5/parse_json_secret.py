from security_client import secret_manager_client, secret_version_path
from security_models import decode_secret_bytes, parse_json_payload


def parse_json_secret(secret_id: str = "json-secret"):
    client = secret_manager_client()
    response = client.access_secret_version(
        request={"name": secret_version_path(secret_id)}
    )
    return parse_json_payload(decode_secret_bytes(response.payload.data))
