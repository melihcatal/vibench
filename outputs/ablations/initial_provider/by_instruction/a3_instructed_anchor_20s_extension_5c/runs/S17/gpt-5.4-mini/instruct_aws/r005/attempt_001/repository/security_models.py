import base64
from dataclasses import dataclass
from typing import Any, Dict, Optional


def b64e(data: bytes) -> str:
    return base64.b64encode(data).decode()


def b64d(data: str) -> bytes:
    return base64.b64decode(data.encode())


@dataclass
class KeyRequest:
    key_id: str
    plaintext: bytes
    encryption_context: Optional[Dict[str, str]] = None


@dataclass
class KeyResponse:
    key_id: str
    ciphertext: bytes
    encryption_context: Optional[Dict[str, str]] = None


def normalize_context(context: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not context:
        return {}
    return {str(k): str(v) for k, v in context.items()}
