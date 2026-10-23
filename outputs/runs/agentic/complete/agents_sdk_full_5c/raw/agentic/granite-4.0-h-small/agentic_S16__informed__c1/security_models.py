from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class SecretSpec:
    """Model for a secret request, capturing all needed fields.
    Attributes:
        secret_id (str): Identifier of the secret in the provider.
        version (str | None): Specific version to retrieve; None for latest.
        expected_fields (list[str]): List of keys expected in the parsed JSON payload.
    """
    secret_id: str
    version: str | None = None
    expected_fields: list[str] = dataclass.field(default_factory=list)

@dataclass
class SecretResponse:
    """Normalized response model for a secret retrieval.
    Attributes:
        data (dict): Raw secret payload returned by the provider (as dict).
        retrieved_at (str): ISO timestamp of retrieval.
        version (str | None): Version identifier retrieved.
    """
    data: dict
    retrieved_at: str
    version: str | None

    def validate(self):
        """Check that all expected fields are present in the retrieved data.
        Raises:
            KeyError: If any expected field is missing.
        """
        for field in self.expected_fields:
            if field not in self.data:
                raise KeyError(f'Expected field {field} missing from secret data')
