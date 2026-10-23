from typing import TypedDict, Any

class EncryptRequest(TypedDict):
    plaintext: str
    key_id: str

class EncryptResponse(TypedDict):
    ciphertext_blob: bytes

class DecryptRequest(TypedDict):
    ciphertext_blob: bytes

class DecryptResponse(TypedDict):
    plaintext: str

class EnvelopeEncryptRequest(TypedDict):
    plaintext: str
    key_id: str

class EnvelopeEncryptResponse(TypedDict):
    encrypted_data_key: bytes
    iv: bytes
    ciphertext: bytes

class SignRequest(TypedDict):
    message: str
    key_id: str
    digest_algorithm: str

class SignResponse(TypedDict):
    signature: bytes

class VerifyRequest(TypedDict):
    message: str
    signature: bytes
    key_id: str
    digest_algorithm: str

class VerifyResponse(TypedDict):
    signature_valid: bool
