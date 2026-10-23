"""Data models for security operations."""
from dataclasses import dataclass

@dataclass
class EncryptionRequest:
    plaintext: bytes

@dataclass
class EncryptionResponse:
    ciphertext: str  # base64 encoded

@dataclass
class DecryptionRequest:
    ciphertext: str  # base64 encoded

@dataclass
class DecryptionResponse:
    plaintext: bytes

@dataclass
class EnvelopeEncryptionRequest:
    plaintext: bytes

@dataclass
class EnvelopeEncryptionResponse:
    encrypted_data: str      # base64 encoded
    encrypted_data_key: str  # base64 encoded

@dataclass
class SigningRequest:
    message: bytes

@dataclass
class SigningResponse:
    message: bytes
    signature: str # base64 encoded
