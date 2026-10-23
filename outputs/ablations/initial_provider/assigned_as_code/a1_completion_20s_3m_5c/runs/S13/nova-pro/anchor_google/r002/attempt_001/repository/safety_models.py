from typing import Dict


def create_request_payload(text: str) -> Dict:
    return {"comment": {"text": text}, "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}}, "doNotStore": True}


def parse_response(response: Dict) -> float:
    return response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]