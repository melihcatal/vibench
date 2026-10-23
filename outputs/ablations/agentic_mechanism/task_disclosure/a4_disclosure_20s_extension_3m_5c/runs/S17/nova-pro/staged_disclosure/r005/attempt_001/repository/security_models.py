from typing import Any, Dict

def create_key_request(key_name: str, key_type: str) -> Dict[str, Any]:
    return {
        'keyName': key_name,
        'keyType': key_type,
    }

def encrypt_request(plaintext: str, key_id: str) -> Dict[str, Any]:
    return {
        'plaintext': plaintext,
        'keyId': key_id,
    }

def decrypt_request(ciphertext: str, key_id: str) -> Dict[str, Any]:
    return {
        'ciphertext': ciphertext,
        'keyId': key_id,
    }

def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    normalized = {}
    for key, value in response.items():
        normalized[key.lower()] = value
    return normalized