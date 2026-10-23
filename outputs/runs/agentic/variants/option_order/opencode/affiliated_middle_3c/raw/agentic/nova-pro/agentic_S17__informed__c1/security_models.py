from typing import Any, Dict


def normalize_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "ciphertext": response.get("CiphertextBlob", ""),
        "plaintext": response.get("Plaintext", ""),
        "signature": response.get("Signature", ""),
    }
