import json
from typing import Any, Dict


# Local request/response models for Secret Management operations
class SecretRequest:
    """Base class for secret fetch requests."""

    def __init__(self, secret_id: str, version_stage: str = "AWSCURRENT"):
        self.secret_id = secret_id
        self.version_stage = version_stage
        self.payload = {"SecretId": secret_id, "VersionStage": version_stage}

    def to_dict(self) -> Dict[str, Any]:
        return self.payload


class SecretResponse:
    """Container for the normalized secret data returned by providers."""

    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        self.data = json.loads(raw["SecretString"])

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)


# Normalization helper for AWS responses
def normalize_response(response: Dict[str, Any]) -> SecretResponse:
    """Convert AWS Secrets Manager response to a SecretResponse object."""
    if "SecretString" not in response:
        raise ValueError("Missing SecretString in response")
    return SecretResponse(response)
