import os
from typing import TypedDict

# Define request, response, and normalized types for Same-scenario encryption


class EncryptionRequest(TypedDict):
    plaintext: bytes
    key_id: str


class EncryptionResponse(TypedDict):
    ciphertext: bytes
    encryption_context: dict | None


class DecryptionRequest(TypedDict):
    ciphertext: bytes
    key_id: str


class DecryptionResponse(TypedDict):
    plaintext: bytes


class DataKeyRequest(TypedDict):
    key_id: str
    key_spec: str | None


class DataKeyResponse(TypedDict):
    plaintext: bytes
    ciphertext: bytes


class KeyMetadataResponse(TypedDict):
    arn: str
    creation_date: str
    enabled: bool
    key_usage: str
