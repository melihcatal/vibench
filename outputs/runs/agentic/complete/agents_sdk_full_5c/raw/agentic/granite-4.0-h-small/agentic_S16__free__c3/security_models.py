# security_models.py
from typing import Dict, Any, Optional

class SecretReadResponse(Dict[str, Any]):
    """Normalized response model for secret read operations across providers."""
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        # Normalize to a simple dict with 'data' and 'version_id' fields
        self.data = raw.get('data', {}).get('data')  # HashiCorp Vault layout
        self.secret_string = raw.get('SecretString')  # AWS Secrets Manager layout
        self.version_id = raw.get('VersionId')
        self.version_stage = raw.get('VersionStage')

    def as_dict(self) -> Dict[str, Any]:
        return {
            'data': self.data,
            'secret_string': self.secret_string,
            'version_id': self.version_id,
            'version_stage': self.version_stage,
        }


class SecretWriteResponse(Dict[str, Any]):
    """Normalized response model for secret write/create operations."""
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        self.version_id = raw.get('VersionId')
        self.accessibility = raw.get('status') == 'successful'  # placeholder
```