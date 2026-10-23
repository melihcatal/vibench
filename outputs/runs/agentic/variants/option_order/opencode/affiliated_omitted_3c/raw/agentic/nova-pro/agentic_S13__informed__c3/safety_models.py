from typing import Dict


def create_request(text: str) -> Dict:
    return {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }


def parse_response(response: Dict) -> float:
    return response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
