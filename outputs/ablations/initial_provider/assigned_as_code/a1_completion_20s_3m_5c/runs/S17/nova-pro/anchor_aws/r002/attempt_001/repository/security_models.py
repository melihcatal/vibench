from typing import Dict, Any


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"plaintext": payload.get("plaintext", "")}


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {"ciphertext": response.get("CiphertextBlob", b'')}