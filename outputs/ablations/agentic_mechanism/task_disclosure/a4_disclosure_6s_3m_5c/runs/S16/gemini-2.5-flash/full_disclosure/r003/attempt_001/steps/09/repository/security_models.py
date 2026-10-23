
import dataclasses
from typing import Optional

@dataclasses.dataclass
class SecretRequest:
    secret_name: str
    version_id: Optional[str] = None

@dataclasses.dataclass
class SecretResponse:
    secret_name: str
    version_id: str
    secret_value: str
    created_at: str

class NormalizationHelper:
    @staticmethod
    def normalize_secret_name(name: str) -> str:
        """Normalizes a secret name to a consistent format."""
        return name.lower().replace(" ", "_").replace("-", "_")
