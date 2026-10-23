from typing import List, Dict, Any

class ModerationResponse:
    def __init__(self, text: str, categories: Dict[str, float], decision: str, raw_response: Any = None):
        self.text = text
        self.categories = categories
        self.decision = decision
        self.raw_response = raw_response

class BatchModerationRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts

class BatchModerationResponse:
    def __init__(self, results: List[ModerationResponse]):
        self.results = results

class RedactionResponse:
    def __init__(self, original_text: str, redacted_text: str, categories: Dict[str, float], spans: List[Dict[str, Any]]):
        self.original_text = original_text
        self.redacted_text = redacted_text
        self.categories = categories
        self.spans = spans
