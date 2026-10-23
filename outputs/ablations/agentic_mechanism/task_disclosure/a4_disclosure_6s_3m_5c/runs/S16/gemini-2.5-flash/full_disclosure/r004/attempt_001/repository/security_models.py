from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class SecretRequest(BaseModel):
    project_id: str
    secret_id: str

class SecretVersionRequest(SecretRequest):
    version_id: str = "latest"

class SecretMetadata(BaseModel):
    name: str
    project_id: str
    secret_id: str
    create_time: datetime
    labels: Optional[Dict[str, str]] = None

class SecretVersion(BaseModel):
    name: str
    version_id: str
    secret_id: str
    create_time: datetime
    destroy_time: Optional[datetime] = None
    state: str
    payload_data: Optional[str] = None # Base64 encoded secret data

class Secret(BaseModel):
    name: str
    secret_id: str
    project_id: str
    replication_status: Optional[Dict[str, Any]] = None
    # Add other relevant fields for a secret

def normalize_secret_name(full_secret_name: str) -> Dict[str, str]:
    """
    Normalizes a full secret name into its components.
    Expected format: projects/PROJECT_ID/secrets/SECRET_ID
    """
    parts = full_secret_name.split('/')
    if len(parts) == 4 and parts[0] == "projects" and parts[2] == "secrets":
        return {
            "project_id": parts[1],
            "secret_id": parts[3]
        }
    raise ValueError(f"Invalid secret name format: {full_secret_name}")

def normalize_secret_version_name(full_secret_version_name: str) -> Dict[str, str]:
    """
    Normalizes a full secret version name into its components.
    Expected format: projects/PROJECT_ID/secrets/SECRET_ID/versions/VERSION_ID
    """
    parts = full_secret_version_name.split('/')
    if len(parts) == 6 and parts[0] == "projects" and parts[2] == "secrets" and parts[4] == "versions":
        return {
            "project_id": parts[1],
            "secret_id": parts[3],
            "version_id": parts[5]
        }
    raise ValueError(f"Invalid secret version name format: {full_secret_version_name}")
