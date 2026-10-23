from security_client import access_secret
from security_models import SecretRef, parse_json_payload


def parse_json_secret(project_id: str, secret_id: str, version: str = "latest"):
    secret_text = access_secret(SecretRef(project_id=project_id, secret_id=secret_id, version=version))
    return parse_json_payload(secret_text)
