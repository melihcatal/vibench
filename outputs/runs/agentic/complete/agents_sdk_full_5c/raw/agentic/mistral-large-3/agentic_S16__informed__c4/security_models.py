from typing import Dict, Any, Optional
import json


class SecretResponse:
    """Normalized secret response model."""

    def __init__(
        self,
        value: str,
        name: str,
        version: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.value = value
        self.name = name
        self.version = version
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": self.value,
            "name": self.name,
            "version": self.version,
            "metadata": self.metadata,
        }


class JSONSecretResponse(SecretResponse):
    """Normalized JSON secret response model."""

    def __init__(
        self,
        value: Dict[str, Any],
        name: str,
        version: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            value=json.dumps(value),
            name=name,
            version=version,
            metadata=metadata,
        )
        self.parsed_value = value

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["parsed_value"] = self.parsed_value
        return base