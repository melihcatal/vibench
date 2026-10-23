
from typing import Optional, Dict, Any
from pydantic import BaseModel

class SecretManagerRequest(BaseModel):
    project_id: str
    secret_id: str

class CreateSecretRequest(SecretManagerRequest):
    replication_policy: Dict[str, Any] = {"automatic": {}}
    labels: Optional[Dict[str, str]] = None

class AddSecretVersionRequest(SecretManagerRequest):
    payload: str

class AccessSecretVersionRequest(SecretManagerRequest):
    version_id: str = "latest"

class SecretVersion(BaseModel):
    name: str
    create_time: str
    state: str

class Secret(BaseModel):
    name: str
    create_time: str
    replication: Dict[str, Any]
    labels: Optional[Dict[str, str]] = None
    versions: Optional[list[SecretVersion]] = None

def normalize_secret_name(project_id: str, secret_id: str) -> str:
    return f"projects/{project_id}/secrets/{secret_id}"

def normalize_secret_version_name(project_id: str, secret_id: str, version_id: str) -> str:
    return f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
