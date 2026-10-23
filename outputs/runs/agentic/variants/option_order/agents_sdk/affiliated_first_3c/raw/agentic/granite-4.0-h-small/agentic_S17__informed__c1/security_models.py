from dataclasses import dataclass
from typing import ByteString, Any, Dict

@dataclass

class EncryptRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    plaintext: ByteString
    additional_auth_data: ByteString = b""

@dataclass
class EncryptResponse:
    ciphertext: ByteString

@dataclass
class DecryptRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    ciphertext: ByteString
    additional_auth_data: ByteString = b""

@dataclass
class DecryptResponse:
    plaintext: ByteString

@dataclass
class EnvelopeEncryptRequest:
    plaintext: ByteString
    master_key_name: str

@dataclass
class EnvelopeEncryptResponse:
    ciphertext: ByteString
    encrypted_dek: ByteString
    nonce: ByteString

@dataclass
class SignRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    message: ByteString

@dataclass
class SignResponse:
    signature: ByteString

@dataclass
class VerifyRequest:
    project_id: str
    location_id: str
    key_ring_id: str
    crypto_key_id: str
    message: ByteString
    signature: ByteString

@dataclass
class VerifyResponse:
    is_valid: bool

# Normalization helper – converts legacy dicts to dataclasses for consistency
def normalize_to_envelope_encrypt(inp: Dict[str, Any]) -> EnvelopeEncryptRequest:
    return EnvelopeEncryptRequest(**inp)

# Validation helper (simple)def validate_envelope_request(req: EnvelopeEncryptRequest):
    assert req.plaintext, "Plaintext must not be empty"
    assert req.master_key_name, "Master key name must be provided"
