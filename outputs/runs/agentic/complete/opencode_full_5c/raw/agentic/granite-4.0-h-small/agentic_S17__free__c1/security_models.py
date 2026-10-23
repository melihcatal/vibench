# [HELPER] security_models.py
# Local request/response data models for key management and encryption tasks
from typing import TypedDict, BinaryIO, Any


class EncryptionRequest(TypedDict):
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    plaintext: bytes


class DecryptionRequest(TypedDict):
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    ciphertext: bytes


class EnvelopeEncryptionResult(TypedDict):
    ciphertext: str  # base64 string
    iv: str  # base64 string
    wrapped_key: str  # base64 string (wrapped data key)
    tag: str  # base64 string (GCM auth tag)


class SignRequest(TypedDict):
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    message: bytes


class SignatureResult(TypedDict):
    signature: bytes


class VerifyRequest(TypedDict):
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    message: bytes
    signature: bytes


class VerifyResult(TypedDict):
    success: bool


class Config(TypedDict):
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    service_account_path: str | None  # optional path to service account JSON


def load_config_from_env() -> Config:
    """Load configuration from environment variables.

    Returns a dict-like Config. Missing optional service_account_path defaults to None.
    """
    return {
        "project_id": os.getenv("KMS_PROJECT_ID"),
        "location_id": os.getenv("KMS_LOCATION_ID"),
        "key_ring_id": os.getenv("KMS_KEY_RING_ID"),
        "crypto_key_id": os.getenv("KMS_CRYPTO_KEY_ID"),
        "service_account_path": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
    }


# Simple helper to serialize a model for logging


def serialize(model: Any) -> str:
    return str(model)


# Example usage (demo only)
if __name__ == "__main__":
    cfg = load_config_from_env()
    print("Loaded config:", serialize(cfg))
