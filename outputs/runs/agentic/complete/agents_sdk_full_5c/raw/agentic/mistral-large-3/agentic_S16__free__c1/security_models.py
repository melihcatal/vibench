from typing import Dict, Any, Optional
from pydantic import BaseModel

class SecretResponse(BaseModel):
    """Normalized response model for secret retrieval."""
    
    value: str
    metadata: Optional[Dict[str, Any]] = None
    version: Optional[str] = None


class JSONSecretResponse(BaseModel):
    """Normalized response model for JSON-formatted secrets."""
    
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None
    version: Optional[str] = None


def normalize_google_secret(value: str, version: str) -> SecretResponse:
    """Normalizes a Google Cloud Secret Manager response."""
    return SecretResponse(value=value, version=version)


def normalize_azure_secret(value: str, name: str) -> SecretResponse:
    """Normalizes an Azure Key Vault response."""
    return SecretResponse(value=value, metadata={"name": name})


def normalize_aws_secret(data: Dict[str, Any], secret_name: str) -> JSONSecretResponse:
    """Normalizes an AWS Secrets Manager response."""
    return JSONSecretResponse(data=data, metadata={"name": secret_name})