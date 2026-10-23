from typing import Dict, Any


def normalize_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"comment": {"text": payload["text"]}, "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True}


def parse_response(response: Dict[str, Any]) -> float:
    return response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]