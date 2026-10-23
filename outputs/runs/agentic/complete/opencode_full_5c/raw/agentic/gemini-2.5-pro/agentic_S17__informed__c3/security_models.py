from pydantic import BaseModel
from typing import Optional, Dict


class EncryptRequest(BaseModel):
    key_id: str
    plaintext: bytes
    encryption_context: Optional[Dict[str, str]] = None


class EncryptResponse(BaseModel):
    ciphertext: bytes
    key_id: str
    success: bool = True


class DecryptRequest(BaseModel):
    key_id: str
    ciphertext: bytes
    encryption_context: Optional[Dict[str, str]] = None


class DecryptResponse(BaseModel):
    plaintext: bytes
    key_id: str
    success: bool = True


class EnvelopeEncryptRequest(BaseModel):
    key_id: str
    plaintext: bytes


class EnvelopeEncryptResponse(BaseModel):
    ciphertext: bytes
    encrypted_data_key: bytes


class SignRequest(BaseModel):
    key_id: str
    message: bytes
    signing_algorithm: str


class SignResponse(BaseModel):
    signature: bytes
    key_id: str


class VerifyRequest(BaseModel):
    key_id: str
    message: bytes
    signature: bytes
    signing_algorithm: str


class VerifyResponse(BaseModel):
    signature_valid: bool
    key_id: str
