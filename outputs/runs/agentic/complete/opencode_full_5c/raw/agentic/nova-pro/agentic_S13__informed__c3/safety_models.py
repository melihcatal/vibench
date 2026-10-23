from typing import Dict


def normalize_request(text: str) -> Dict:
    return {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
    }


def parse_response(response: Dict) -> float:
    return (
        response.get("attributeScores", {})
        .get("TOXICITY", [{}])[0]
        .get("summaryScore", {})
        .get("value", 0)
    )
