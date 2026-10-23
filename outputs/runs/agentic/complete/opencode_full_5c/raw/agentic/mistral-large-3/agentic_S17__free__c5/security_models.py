from typing import Dict, Any, Optional
from pydantic import BaseModel
import json


class EncryptionRequest(BaseModel):
    plaintext: str
    key_id: Optional[str] = None
    context: Optional[Dict[str, str]] = None


class EncryptionResponse(BaseModel):
    ciphertext: str
    key_id: str
    algorithm: str
    encrypted_key: Optional[str] = None


class DecryptionRequest(BaseModel):
    ciphertext: str
    key_id: Optional[str] = None
    encrypted_key: Optional[str] = None
    context: Optional[Dict[str, str]] = None


class DecryptionResponse(BaseModel):
    plaintext: str
    key_id: str
    algorithm: str


class SigningRequest(BaseModel):
    data: str
    key_id: Optional[str] = None


class SigningResponse(BaseModel):
    signature: str
    key_id: str
    algorithm: str


class VerificationRequest(BaseModel):
    data: str
    signature: str
    key_id: Optional[str] = None


class VerificationResponse(BaseModel):
    is_valid: bool
    key_id: str


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized = payload.copy()
    if "plaintext" in normalized and isinstance(normalized["plaintext"], str):
        normalized["plaintext"] = normalized["plaintext"].encode()
    if "ciphertext" in normalized and isinstance(normalized["ciphertext"], str):
        normalized["ciphertext"] = normalized["ciphertext"].encode()
    if "data" in normalized and isinstance(normalized["data"], str):
        normalized["data"] = normalized["data"].encode()
    if "signature" in normalized and isinstance(normalized["signature"], str):
        normalized["signature"] = normalized["signature"].encode()
    return normalized


def serialize_response(response: Dict[str, Any]) -> str:
    serializable = {}
    for k, v in response.items():
        if isinstance(v, bytes):
            serializable[k] = v.decode()
        else:
            serializable[k] = v
    return json.dumps(serializable)
