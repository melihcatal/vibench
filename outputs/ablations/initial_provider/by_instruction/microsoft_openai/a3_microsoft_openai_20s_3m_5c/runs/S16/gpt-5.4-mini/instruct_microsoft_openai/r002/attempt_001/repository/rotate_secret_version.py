from security_client import create_secret_client
from security_models import SecretRequest, SecretResponse, normalize_secret_payload


def rotate_secret_version(secret_name: str, version: str = None, stage: str = None) -> SecretResponse:
    client = create_secret_client()
    request = SecretRequest(name=secret_name, version=version, stage=stage)
    if request.version:
        secret = client.get_secret(request.name, version=request.version)
    else:
        secret = client.get_secret(request.name)
    data = normalize_secret_payload(secret)
    return SecretResponse(name=data.get("name", request.name), value=data["value"], version=data.get("version"))
