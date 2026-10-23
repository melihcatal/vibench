import os
import json
from typing import Optional, Dict, Any
from google.cloud import kms_v1
from google.auth import default


class SecurityClient:
    """Client helper utilities for Key Management and Encryption."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self._kms_client = None
        self._credentials = None

    @property
    def kms_client(self) -> kms_v1.KeyManagementServiceClient:
        """Get or create KMS client."""
        if self._kms_client is None:
            self._kms_client = kms_v1.KeyManagementServiceClient()
        return self._kms_client

    def get_credentials(self):
        """Get Google Cloud credentials."""
        if self._credentials is None:
            self._credentials, _ = default()
        return self._credentials

    def build_key_name(
        self, location: str, key_ring: str, key_name: str, version: Optional[str] = None
    ) -> str:
        """Build a fully qualified KMS key name."""
        if version:
            return f"projects/{self.project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{key_name}/cryptoKeyVersions/{version}"
        else:
            return f"projects/{self.project_id}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{key_name}"

    def load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load security configuration from file or environment."""
        config = {
            "default_location": os.environ.get("GCP_KMS_LOCATION", "global"),
            "default_key_ring": os.environ.get("GCP_KMS_KEY_RING", "default-key-ring"),
            "default_encryption_key": os.environ.get(
                "GCP_KMS_ENCRYPTION_KEY", "default-encryption-key"
            ),
            "default_signing_key": os.environ.get(
                "GCP_KMS_SIGNING_KEY", "default-signing-key"
            ),
            "provider": "google-cloud-kms",
        }

        if config_path and os.path.exists(config_path):
            with open(config_path, "r") as f:
                file_config = json.load(f)
                config.update(file_config)

        return config

    def normalize_payload(self, payload: Any) -> str:
        """Normalize payload to string for encryption."""
        if isinstance(payload, str):
            return payload
        elif isinstance(payload, dict) or isinstance(payload, list):
            return json.dumps(payload, separators=(",", ":"))
        else:
            return str(payload)

    def parse_encryption_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and normalize encryption result."""
        normalized = {
            "provider": result.get("provider", "google-cloud-kms"),
            "key_name": result.get("key_name"),
            "algorithm": result.get("algorithm"),
            "timestamp": result.get("timestamp") or self._get_timestamp(),
        }

        if "ciphertext" in result:
            normalized["ciphertext"] = result["ciphertext"]
        if "encrypted_dek" in result:
            normalized["encrypted_dek"] = result["encrypted_dek"]
        if "iv" in result:
            normalized["iv"] = result["iv"]
        if "signature" in result:
            normalized["signature"] = result["signature"]

        return normalized

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime

        return datetime.utcnow().isoformat() + "Z"
