import os
from typing import Optional

from security_client import get_secret_manager_client, get_secret_name
from security_models import SecretRotationRequest, normalize_secret_payload

# HashiCorp Vault integration via hvac
import hvac


def rotate_secret_version(secret_path: Optional[str] = None, version: Optional[str] = None, mount_point: Optional[str] = None):
    client = get_secret_manager_client(provider="vault", url=os.getenv("VAULT_ADDR"))
    path = secret_path or os.getenv("VAULT_SECRET_PATH", "secret/data/app")
    request = SecretRotationRequest(secret_path=path, version=version)
    response = client.secrets.kv.v2.read_secret_version(path=request.secret_path, version=request.version and int(request.version), mount_point=mount_point or os.getenv("VAULT_MOUNT_POINT", "secret"))
    data = response["data"]["data"]
    return normalize_secret_payload(data)
