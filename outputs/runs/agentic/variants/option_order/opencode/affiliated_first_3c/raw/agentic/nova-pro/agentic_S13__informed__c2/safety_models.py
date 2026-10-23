from typing import Dict, List


class SafetyRequest:
    def __init__(self, text: str):
        self.text = text


class SafetyResponse:
    def __init__(self, toxic_content_detected: bool):
        self.toxic_content_detected = toxic_content_detected


def normalize_response(response: Dict) -> SafetyResponse:
    return SafetyResponse(response["ToxicContentDetected"])
