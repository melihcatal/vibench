from security_client import fetch_secret
from security_models import SecretRequest


def rotate_secret_version(secret_name: str, version_stage: str = "AWSPENDING") -> str:
    resp = fetch_secret(SecretRequest(name=secret_name, version_stage=version_stage))
    if not resp.secret_string:
        raise ValueError("Secret string is empty")
    return resp.secret_string
