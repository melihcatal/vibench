from typing import Dict, List


class ModerationRequest:
    def __init__(self, text: str):
        self.text = text


class ModerationResponse:
    def __init__(self, unsafe: bool, safety_score: float, redacted_text: str):
        self.unsafe = unsafe
        self.safety_score = safety_score
        self.redacted_text = redacted_text


def normalize_response(response: Dict) -> ModerationResponse:
    return ModerationResponse(
        unsafe=response["unsafe"],
        safety_score=response["safety_score"],
        redacted_text=response["redacted_text"],
    )
