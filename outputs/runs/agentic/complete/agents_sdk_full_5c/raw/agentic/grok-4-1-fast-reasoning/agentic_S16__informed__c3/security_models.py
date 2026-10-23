from typing import Any, Dict, Optional
from pydantic import BaseModel

class ApiKeySecret(BaseModel):
    api_key: str

class DbCredentials(BaseModel):
    host: str
    port: Optional[int] = None
    username: str
    password: str
    database: Optional[str] = None

class JsonSecret(BaseModel):
    data: Dict[str, Any]

class SecretVersionInfo(BaseModel):
    version_id: str
    secret_value: str
    created_date: Optional[str] = None
