from typing import List, Dict, Any

class ModerationResult:
    def __init__(self, text: str, categories: Dict[str, float], decision: str = "allow"):
        self.text = text
        self.categories = categories
        self.decision = decision

class BatchModerationRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts

class BatchModerationResponse:
    def __init__(self, results: List[ModerationResult]):
        self.results = results

class RedactionResult:
    def __init__(self, original_text: str, redacted_text: str, detections: List[Dict[str, Any]]):
        self.original_text = original_text
        self.redacted_text = redacted_text
        self.detections = detections
