from typing import Dict, Any

def normalize_encrypt_response(response: Dict[str, Any]) -> bytes:
    return response['CiphertextBlob']

def normalize_decrypt_response(response: Dict[str, Any]) -> bytes:
    return response['Plaintext']

def normalize_sign_response(response: Dict[str, Any]) -> bytes:
    return response['Signature']

def normalize_verify_response(response: Dict[str, Any]) -> bool:
    return response['SignatureValid']