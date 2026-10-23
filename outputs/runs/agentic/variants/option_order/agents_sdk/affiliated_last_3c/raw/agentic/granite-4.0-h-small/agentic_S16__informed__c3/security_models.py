from __future__ import annotations

import json
from typing import Any, Dict, List

from security_client import SecretClient


class SecretModel:
    """Base model for a secret object returned by a secret manager.

    Attributes:
        name: Human‑readable name/ARN of the secret.
        arn: Full ARN if available.
        version_id: Identifier of the version that was retrieved.
        payload: The raw secret data (usually a dict after JSON parsing).
    """

    def __init__(
        self,
        name: str,
        arn: str | None = None,
        version_id: str | None = None,
        payload: Any = None,
    ) -> None:
        self.name = name
        self.arn = arn
        self.version_id = version_id
        self.payload = payload if payload is not None else {}


class SecretResponse:
    """Normalized response wrapper used across same‑scenario functions.

    Normalization converts any provider‑specific payload into a SecretModel instance.
    """

    @staticmethod
    def from_client_response(client: SecretClient, raw_response: dict) -> SecretResponse:
        """Build a SecretResponse from a provider SDK call result.

        Args:
            client: The SecretClient implementation (e.g., boto3 client wrapper).
            raw_response: The dict returned by get_secret_value or similar.
        """
        # Extract name/ARN – Secrets Manager puts it in 'ARN' and 'Name' fields
        name = raw_response.get('ARN') or raw_response.get('Name')
        # Assume version identifier is stored in 'VersionId' if present, else None
        version_id = raw_response.get('VersionId')
        # The secret payload may be a JSON string (SecretString) or already parsed JSON
        secret_str = raw_response.get('SecretString')
        payload = json.loads(secret_str) if secret_str else {}
        return SecretResponse(name, version_id=version_id, payload=payload)


class RotatedSecret(SecretModel):
    """Model representing a secret after a rotation operation.

    Adds fields useful for rotation audits.
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.rotation_timestamp = None  # populated by later‑step utilities

    def set_rotation_timestamp(self, ts: str) -> None:
        self.rotation_timestamp = ts


def normalize_secret_response(client: SecretClient, raw: dict) -> SecretResponse:
    """Normalize any provider's raw get_secret_value output to our canonical model.
    """
    return SecretResponse.from_client_response(client, raw)


def list_secrets(client: SecretClient, filter_name: str | None = None) -> List[str]:
    """Utility to list secret identifiers using the generic SecretClient protocol.
    """
    resp = client.list_secrets()
    return [s['Name'] for s in resp.get('SecretList', [])]
