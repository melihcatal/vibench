from typing import Dict


class SafetyRequest:
    def __init__(self, text: str):
        self.text = text


class SafetyResponse:
    def __init__(self, toxicity_score: float):
        self.toxicity_score = toxicity_score


def normalize_response(response: Dict):
    return SafetyResponse(
        response["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    )
