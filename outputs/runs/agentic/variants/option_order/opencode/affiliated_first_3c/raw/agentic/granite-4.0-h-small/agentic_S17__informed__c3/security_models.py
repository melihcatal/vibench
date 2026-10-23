import os
from typing import Dict, List
from security_client import SecurityClient

class SecurityModels:
    """Local request, response, and normalization models for Key Management and Encryption.",
    REQUEST_ENCRYPT = {
        "type": "object",
        "properties": {
            "plaintext": {"type": "string"},
            "key_id": {"type": "string"}
        },
        "required": ["plaintext", "key_id"]
    }

    RESPONSE_ENCRYPT = {
        "type": "object",
        "properties": {
            "ciphertext": {"type": "string"},
            "data_key": {"type": "string"},
            "key_id": {"type": "string"}
        },
        "required": ["ciphertext", "data_key", "key_id"]
    }

    REQUEST_DECRYPT = {
        "type": "object",
        "properties": {
            "ciphertext": {"type": "string"},
            "key_id": {"type": "string"}
        },
        "required": ["ciphertext", "key_id"]
    }

    RESPONSE_DECRYPT = {
        "type": "object",
        "properties": {
            "plaintext": {"type": "string"},
            "key_id": {"type": "string"}
        },
        "required": ["plaintext", "key_id"]
    }

    # Additional request/response schemas can be added similarly
    # Example: REQUEST_ENVELOPE_ENCRYPT, RESPONSE_ENVELOPE_ENCRYPT, etc.
