from pydantic import BaseModel
from typing import Optional, Union

class EncryptionRequest(BaseModel):
    plaintext: bytes
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str

class EncryptionResponse(BaseModel):
    ciphertext: bytes
    key_version: str
    provider: str
    model: str

class DecryptionRequest(BaseModel):
    ciphertext: bytes
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str

class DecryptionResponse(BaseModel):
    plaintext: bytes
    key_version: str
    provider: str
    model: str

class EnvelopeEncryptionRequest(BaseModel):
    plaintext: bytes
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str

class EnvelopeEncryptionResponse(BaseModel):
    ciphertext: bytes
    encrypted_dek: bytes
    iv: bytes
    provider: str
    model: str

class SigningRequest(BaseModel):
    data: bytes
    digest: bytes
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str

class SigningResponse(BaseModel):
    signature: bytes
    provider: str
    model: str

class VerificationRequest(BaseModel):
    data: bytes
    digest: bytes
    signature: bytes
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str

class VerificationResponse(BaseModel):
    is_valid: bool
    provider: str
    model: str