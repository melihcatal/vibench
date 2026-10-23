from typing import Dict, List


class TextSegment:
    def __init__(self, text: str):
        self.text = text


class ToxicityResult:
    def __init__(self, toxicity: float):
        self.toxicity = toxicity


class ModerationResult:
    def __init__(self, text: str, toxicity: float):
        self.text = text
        self.toxicity = toxicity


def normalize_payload(payload: Dict) -> TextSegment:
    return TextSegment(payload['text'])


def parse_response(response: Dict) -> ToxicityResult:
    return ToxicityResult(response['ResultList'][0]['Toxicity'])