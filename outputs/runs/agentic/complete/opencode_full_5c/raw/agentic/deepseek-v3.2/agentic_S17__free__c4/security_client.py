import os
import json
import base64
import hashlib
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
import boto3
from botocore.exceptions import ClientError
from google.cloud import kms
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient


@dataclass
class SecurityConfig:
    """Configuration for security operations."""

    aws_region: str = "us-east-1"
    aws_kms_key_id: str = "alias/encryption-key"
    aws_signing_key_id: str = "alias/signing-key"
    gcp_project_id: str = "my-project"
    gcp_key_ring: str = "my-key-ring"
    gcp_key_name: str = "my-key"
    azure_key_vault_url: str = "https://myvault.vault.azure.net"
    azure_key_name: str = "mykey"
    default_provider: str = "aws"
    encryption_algorithm: str = "AES-GCM-256"
    signing_algorithm: str = "RSASSA_PKCS1_V1_5_SHA_256"


class SecurityClient:
    """Client helper for key management and encryption operations."""

    def __init__(self, config: Optional[SecurityConfig] = None):
        self.config = config or self._load_config_from_env()
        self._clients = {}

    def _load_config_from_env(self) -> SecurityConfig:
        """Load configuration from environment variables."""
        return SecurityConfig(
            aws_region=os.environ.get("AWS_REGION", "us-east-1"),
            aws_kms_key_id=os.environ.get("AWS_KMS_KEY_ID", "alias/encryption-key"),
            aws_signing_key_id=os.environ.get(
                "AWS_KMS_SIGNING_KEY_ID", "alias/signing-key"
            ),
            gcp_project_id=os.environ.get("GCP_PROJECT_ID", "my-project"),
            gcp_key_ring=os.environ.get("GCP_KEY_RING", "my-key-ring"),
            gcp_key_name=os.environ.get("GCP_KEY_NAME", "my-key"),
            azure_key_vault_url=os.environ.get(
                "AZURE_KEY_VAULT_URL", "https://myvault.vault.azure.net"
            ),
            azure_key_name=os.environ.get("AZURE_KEY_NAME", "mykey"),
            default_provider=os.environ.get("SECURITY_PROVIDER", "aws"),
            encryption_algorithm=os.environ.get("ENCRYPTION_ALGORITHM", "AES-GCM-256"),
            signing_algorithm=os.environ.get(
                "SIGNING_ALGORITHM", "RSASSA_PKCS1_V1_5_SHA_256"
            ),
        )

    def get_aws_kms_client(self):
        """Get or create AWS KMS client."""
        if "aws_kms" not in self._clients:
            self._clients["aws_kms"] = boto3.client(
                "kms", region_name=self.config.aws_region
            )
        return self._clients["aws_kms"]

    def get_gcp_kms_client(self):
        """Get or create GCP KMS client."""
        if "gcp_kms" not in self._clients:
            self._clients["gcp_kms"] = kms.KeyManagementServiceClient()
        return self._clients["gcp_kms"]

    def get_azure_key_client(self):
        """Get or create Azure Key Vault client."""
        if "azure_key" not in self._clients:
            credential = DefaultAzureCredential()
            self._clients["azure_key"] = KeyClient(
                vault_url=self.config.azure_key_vault_url, credential=credential
            )
        return self._clients["azure_key"]

    def normalize_payload(self, payload: Union[str, bytes, Dict]) -> bytes:
        """Normalize payload to bytes for encryption/signing."""
        if isinstance(payload, str):
            return payload.encode("utf-8")
        elif isinstance(payload, bytes):
            return payload
        elif isinstance(payload, dict):
            return json.dumps(payload, sort_keys=True).encode("utf-8")
        else:
            return str(payload).encode("utf-8")

    def compute_hash(self, data: Union[str, bytes], algorithm: str = "sha256") -> str:
        """Compute hash of data."""
        data_bytes = self.normalize_payload(data)

        if algorithm.lower() == "sha256":
            return hashlib.sha256(data_bytes).hexdigest()
        elif algorithm.lower() == "sha512":
            return hashlib.sha512(data_bytes).hexdigest()
        elif algorithm.lower() == "md5":
            return hashlib.md5(data_bytes).hexdigest()
        else:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    def encode_base64(self, data: Union[str, bytes]) -> str:
        """Base64 encode data."""
        data_bytes = self.normalize_payload(data)
        return base64.b64encode(data_bytes).decode("utf-8")

    def decode_base64(self, encoded: str) -> bytes:
        """Base64 decode data."""
        return base64.b64decode(encoded)

    def parse_encryption_result(self, result: Dict) -> Dict:
        """Parse and validate encryption result."""
        required_fields = ["ciphertext", "provider"]

        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing required field: {field}")

        # Add metadata if not present
        if "timestamp" not in result:
            from datetime import datetime

            result["timestamp"] = datetime.utcnow().isoformat() + "Z"

        if "version" not in result:
            result["version"] = "1.0"

        return result

    def get_full_gcp_key_id(self) -> str:
        """Get full GCP KMS key ID."""
        return f"projects/{self.config.gcp_project_id}/locations/global/keyRings/{self.config.gcp_key_ring}/cryptoKeys/{self.config.gcp_key_name}"

    def get_full_azure_key_id(self) -> str:
        """Get full Azure Key Vault key ID."""
        return f"{self.config.azure_key_vault_url}/keys/{self.config.azure_key_name}"

    def validate_key_id(self, key_id: str, provider: str) -> bool:
        """Validate key ID format for provider."""
        if provider == "aws":
            return key_id.startswith("alias/") or key_id.startswith("arn:aws:kms:")
        elif provider == "gcp":
            return (
                "projects/" in key_id
                and "keyRings/" in key_id
                and "cryptoKeys/" in key_id
            )
        elif provider == "azure":
            return (
                key_id.startswith("https://")
                and "vault.azure.net" in key_id
                and "/keys/" in key_id
            )
        else:
            return True  # Unknown provider, assume valid

    def create_encryption_context(self, purpose: str = "encryption", **kwargs) -> Dict:
        """Create encryption context metadata."""
        context = {
            "purpose": purpose,
            "timestamp": os.environ.get("TIMESTAMP", "2024-01-01T00:00:00Z"),
            "provider": self.config.default_provider,
            "algorithm": self.config.encryption_algorithm,
        }
        context.update(kwargs)
        return context

    def to_dict(self) -> Dict:
        """Convert client configuration to dictionary."""
        return asdict(self.config)


def load_security_config(config_path: Optional[str] = None) -> SecurityConfig:
    """Load security configuration from file or environment."""
    if config_path and os.path.exists(config_path):
        with open(config_path, "r") as f:
            config_data = json.load(f)
            return SecurityConfig(**config_data)

    # Fall back to environment variables
    return SecurityClient().config


def create_security_client(config: Optional[SecurityConfig] = None) -> SecurityClient:
    """Factory function to create security client."""
    return SecurityClient(config)
