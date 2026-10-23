from typing import Optional, Dict, Any
from pydantic import BaseModel


class SecretData(BaseModel):
    name: str
    value: str
    arn: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[Dict[str, str]] = None
    version_id: Optional[str] = None
    created_date: Optional[Any] = None


class RotationStatus(BaseModel):
    secret_name: str
    rotation_enabled: bool
    last_rotated_date: Optional[Any] = None
    next_rotation_date: Optional[Any] = None
