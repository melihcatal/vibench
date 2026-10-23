from dataclasses import dataclass
from typing import Union, Optional, TypedDict, Any
import base64

BytesOrStr = Union[bytes, str]

@dataclass
class KeyConfig:
    key_id: str
    region: str = 'us-east-1'

class EncryptResponse(TypedDict):
    ciphertext_blob: bytes
    key_id: str

class DecryptResponse(TypedDict):
    plaintext: bytes
    key_id: str

def normalize_payload(payload: BytesOrStr) -> bytes:
    if isinstance(payload, str):
        return payload.encode('utf-8')
    return payload

def denormalize_payload(payload: bytes) -> str:
    try:
        return payload.decode('utf-8')
    except UnicodeDecodeError:
        return repr(payload)[:100]
