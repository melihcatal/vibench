from typing import Dict


class SafetyRequest:
    def __init__(self, text: str):
        self.text = text


class SafetyResponse:
    def __init__(self, data: Dict):
        self.safety_score = data.get("safety_score")
        self.redacted_text = data.get("redacted_text")


def normalize_response(response: Dict) -> SafetyResponse:
    return SafetyResponse(response)
