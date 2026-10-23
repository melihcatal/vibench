from typing import Dict

def normalize_payload(payload: Dict) -> Dict:
    return {"plaintext": payload["plaintext"]}

def normalize_response(response: Dict) -> Dict:
    return {"ciphertext": response["ciphertext"]}