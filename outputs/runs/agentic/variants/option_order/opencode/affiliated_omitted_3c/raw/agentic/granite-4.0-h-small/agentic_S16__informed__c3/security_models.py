# HELPER
# security_models.py - Define local request, response, and normalization helpers for Secret Management

from typing import Any, Dict

# Simple request model representing a secret fetch request


class SecretRequest:
    def __init__(self, name: str, project_id: str = None):
        self.name = name  # secret name (without full resource ID)
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")

    def validate(self) -> bool:
        """Basic validation of request fields."""
        if not self.name:
            raise ValueError("Secret name cannot be empty")
        if not self.project_id:
            raise ValueError("Google Cloud project ID must be provided")
        return True


# Simple response wrapper for secret payloads


class SecretResponse:
    def __init__(self, payload: str):
        self.payload = payload

    def as_dict(self) -> Dict[str, Any]:
        """Return the raw payload as a JSON‑parsed dict if possible."""
        try:
            return json.loads(self.payload)
        except json.JSONDecodeError:
            return {"raw": self.payload}


# Helper to normalize secret payloads to a consistent dict format


def normalize_secret(payload: str) -> Dict[str, Any]:
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        return {"value": payload}
