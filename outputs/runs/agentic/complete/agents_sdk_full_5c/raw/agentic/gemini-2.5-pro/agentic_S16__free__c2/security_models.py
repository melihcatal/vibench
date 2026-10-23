from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class DatabaseCredentials(BaseModel):
    """Represents database connection credentials."""
    username: str
    password: str
    engine: str
    host: str
    port: int
    dbname: str

class ApiGatewayConfig(BaseModel):
    """Represents configuration for an API Gateway."""
    api_key: str
    service_url: str
    timeout: int = Field(default=60)

class SecretVersion(BaseModel):
    """Represents a specific version of a secret."""
    data: Dict[str, Any]
    version: int
    created_time: Optional[str] = None
