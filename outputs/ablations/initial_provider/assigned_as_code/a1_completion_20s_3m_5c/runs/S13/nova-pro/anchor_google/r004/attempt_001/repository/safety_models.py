from typing import Dict, List


def normalize_payload(text: str) -> Dict:
    return {"text": text}


def parse_response(response: Dict) -> float:
    return response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]