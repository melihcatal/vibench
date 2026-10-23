import os
from typing import Protocol

# Define type aliases for payloads
PlaintextPayload = str
CiphertextPayload = bytes
SignaturePayload = bytes


# Configuration loader for cloud providers
class KeyManagementConfig:
    """Load provider-specific configuration from environment or credentials file."""

    def __init__(self):
        self._resolve()

    def _resolve(self):
        # Placeholder: in production this would load AWS, GCP, Azure, etc. details
        # For demonstration we expose placeholder attributes
        self.region = os.getenv("AWS_REGION", "us-east-1")
        self.key_id = os.getenv("AWS_KMS_KEY_ID")
        self.token = os.getenv("VAULT_TOKEN")
        self.vault_addr = os.getenv("VAULT_ADDR")


class KeyManagementClient(Protocol):
    """Protocol defining common KMS operations across providers."""

    def generate_data_key(self, key_id: str) -> bytes: ...  # Placeholder

    def encrypt_payload(self, plaintext: str) -> CiphertextPayload: ...  # Placeholder

    def decrypt_payload(
        self, ciphertext: CiphertextPayload
    ) -> PlaintextPayload: ...  # Placeholder

    def sign(self, data: str) -> SignaturePayload: ...  # Placeholder

    def verify(self, data: str, signature: SignaturePayload) -> bool: ...  # Placeholder


# Simple utility for hashing payloads (used by various providers)
def hash_payload(payload: str) -> str:
    return hashlib.sha256(payload.encode()).hexdigest()


# Helper to assert presence of required env vars
def _require_env(*vars):
    missing = [v for v in vars if not os.getenv(v)]
    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}"
        )
