from pydantic import BaseModel
from typing import Optional

class EncryptionRequest(BaseModel):
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    plaintext: str

class EncryptionResponse(BaseModel):
    ciphertext: bytes
    key_version: str

class DecryptionRequest(BaseModel):
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    ciphertext: bytes

class DecryptionResponse(BaseModel):
    plaintext: str

class EnvelopeEncryptionRequest(BaseModel):
    project_id: str
    location_id: str
    key_ring_id: str
    key_key_id: str
    plaintext: str

class EnvelopeEncryptionResponse(BaseModel):
    ciphertext: bytes
    encrypted_dek: bytes
    iv: bytes
    tag: bytes

class SignRequest(BaseModel):
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    digest: bytes

class SignResponse(BaseModel):
    signature: bytes

class VerifyRequest(BaseModel):
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    digest: bytes
    signature: bytes

class VerifyResponse(BaseModel):
    valid: bool