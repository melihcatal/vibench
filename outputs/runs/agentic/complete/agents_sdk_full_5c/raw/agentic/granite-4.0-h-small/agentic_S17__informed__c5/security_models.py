from typing import TypedDict, Optional


class EncryptRequest(TypedDict):
    plaintext: str

class EncryptResponse(TypedDict):
    ciphertext: str

class DecryptRequest(TypedDict):
    ciphertext: str

class DecryptResponse(TypedDict):
    plaintext: str

class SerializeEncryptRequest(TypedDict):
    key_name: str
    plaintext: str

class SerializeDecryptRequest(TypedDict):
    key_name: str
    ciphertext: str

class EnvelopeEncryptRequest(TypedDict):
    payload: bytes
    key_name: str

class EnvelopeEncryptResponse(TypedDict):
    encrypted_data_key: str
    plaintext_data_key: str

class SignOrVerifyRequest(TypedDict):
    input_bytes: bytes
    key_name: str
    sign: bool

class SignOrVerifyResponse(TypedDict):
    signature: Optional[str] = None
    is_valid: Optional[bool] = None
