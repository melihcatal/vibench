from pydantic import BaseModel
from typing import Optional

class EncryptionRequest(BaseModel):
    plaintext: bytes

class EncryptionResponse(BaseModel):
    ciphertext: bytes
    key_id: str
    algorithm: str

class DecryptionRequest(BaseModel):
    ciphertext: bytes

class DecryptionResponse(BaseModel):
    plaintext: bytes
    key_id: str
    algorithm: str

class EnvelopeEncryptionRequest(BaseModel):
    plaintext: bytes

class EnvelopeEncryptionResponse(BaseModel):
    ciphertext: bytes
    encrypted_dek: bytes
    iv: bytes
    key_id: str
    algorithm: str

class SignRequest(BaseModel):
    digest: bytes

class SignResponse(BaseModel):
    signature: bytes
    key_id: str
    algorithm: str

class VerifyRequest(BaseModel):
    digest: bytes
    signature: bytes

class VerifyResponse(BaseModel):
    is_valid: bool
    key_id: str
    algorithm: str