from typing import Union, Dict, Any


def normalize_payload(payload: Union[str, bytes]) -> bytes:
    if isinstance(payload, str):
        return payload.encode("utf-8")
    return payload


def parse_decrypt_response(response: Dict[str, Any]) -> bytes:
    return response["Plaintext"]


def build_envelope(encrypted_key: bytes, ciphertext: bytes) -> Dict[str, bytes]:
    return {"encrypted_key": encrypted_key, "ciphertext": ciphertext}
