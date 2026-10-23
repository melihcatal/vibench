from typing import Dict, Any


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"text": payload["text"]}


def parse_response(response: Dict[str, Any]) -> str:
    return "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)