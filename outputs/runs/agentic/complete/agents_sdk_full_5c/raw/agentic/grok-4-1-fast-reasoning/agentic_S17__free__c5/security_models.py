import base64
import json
from dataclasses import dataclass, asdict
from typing import Union

@dataclass
class CryptoEnvelope:
    encrypted_key: str
    iv: str
    ciphertext: str

def serialize_envelope(envelope: CryptoEnvelope) -> str:
    return json.dumps(asdict(envelope))

def deserialize_envelope(envelope_str: str) -> CryptoEnvelope:
    data = json.loads(envelope_str)
    return CryptoEnvelope(**data)

def normalize_plaintext(plaintext: Union[str, bytes]) -> bytes:
    if isinstance(plaintext, str):
        return plaintext.encode('utf-8')
    return plaintext

def serialize_bytes(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8')

def deserialize_bytes(data_b64: str) -> bytes:
    return base64.b64decode(data_b64)