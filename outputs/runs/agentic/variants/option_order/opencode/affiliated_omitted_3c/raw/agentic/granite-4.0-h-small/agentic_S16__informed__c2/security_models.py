# [HELPER] security_models.py
# Define local request, response, and normalization helpers for Secret Management

from typing import Any, Dict


# Generic response envelope for secret retrieval
class SecretResponse:
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        self.data: Dict[str, Any] | None = None
        self.parse()

    def parse(self) -> None:
        """Extract the useful payload from various provider envelopes."""
        # AWS Secrets Manager example
        if "SecretString" in self.raw:
            self.data = json.loads(self.raw["SecretString"])
        elif "SecretBinary" in self.raw:
            self.data = json.loads(
                base64.b64decode(self.raw["SecretBinary"]).decode("utf-8")
            )
        # Azure Key Vault placeholder
        elif "value" in self.raw:
            self.data = {"value": self.raw["value"]}
        # Google Secret Manager placeholder
        elif "secretData" in self.raw:
            self.data = json.loads(
                base64.b64decode(self.raw["secretData"]).decode("utf-8")
            )
        else:
            self.data = {}

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)


# Normalization helper to flatten nested secret structures into a flat dict


def normalize_secret(raw: Dict[str, Any]) -> Dict[str, str]:
    normalized = {}

    # Simple recursive flatten (depth‑first)
    def _flatten(prefix: str, obj: Any):
        if isinstance(obj, dict):
            for k, v in obj.items():
                _flatten(f"{prefix}.{k}" if prefix else k, v)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                _flatten(f"{prefix}[{i}]", item)
        else:
            normalized[prefix] = str(obj)

    _flatten("", raw)
    return normalized
