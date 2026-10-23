from typing import List, Dict, Any

class TextModerationRequest:
    def __init__(self, text: str):
        self.text = text

class TextModerationResponse:
    def __init__(self, categories: Dict[str, float], is_unsafe: bool):
        self.categories = categories
        self.is_unsafe = is_unsafe

class BatchModerationRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts

class BatchModerationResponse:
    def __init__(self, results: List[TextModerationResponse]):
        self.results = results

class RedactionRequest:
    def __init__(self, text: str):
        self.text = text

class RedactionResponse:
    def __init__(self, redacted_text: str, unsafe_spans: List[Dict[str, Any]]):
        self.redacted_text = redacted_text
        self.unsafe_spans = unsafe_spans

class ThresholdConfig:
    def __init__(self, thresholds: Dict[str, float], decision_threshold: float = 0.5):
        self.thresholds = thresholds
        self.decision_threshold = decision_threshold

class ThresholdDecision:
    def __init__(self, is_allowed: bool, decision_details: Dict[str, Any]):
        self.is_allowed = is_allowed
        self.decision_details = decision_details
