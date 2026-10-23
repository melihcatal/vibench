from pydantic import BaseModel
from typing import Optional

class EncryptRequest(BaseModel):
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    plaintext: bytes

class EncryptResponse(BaseModel):
    ciphertext: bytes

class DecryptRequest(BaseModel):
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    ciphertext: bytes

class DecryptResponse(BaseModel):
    plaintext: bytes

class EnvelopeEncryptRequest(BaseModel):
    project_id: str
    location_id: str
    key_ring_id: str
    key_id: str
    plaintext: bytes

class EnvelopeEncryptResponse(BaseModel):
    ciphertext: bytes
    encrypted_dek: bytes

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