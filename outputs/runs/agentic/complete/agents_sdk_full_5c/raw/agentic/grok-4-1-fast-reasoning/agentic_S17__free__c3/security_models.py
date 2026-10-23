import base64
from typing import Dict, List, Any
from dataclasses import dataclass

def b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8')

def b64decode(data: str) -> bytes:
    return base64.b64decode(data)

def normalize_payload(payload: str) -> bytes:
    return payload.encode('utf-8')

@dataclass
class EnvelopeCiphertext:
    encrypted_key: str
    ciphertext: str
