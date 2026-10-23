from typing import Dict, Any


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    if "plaintext" in payload:
        payload["plaintext"] = payload["plaintext"].encode('utf-8')
    return payload


def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
    if "Plaintext" in response:
        response["Plaintext"] = response["Plaintext"].decode('utf-8')
    return response