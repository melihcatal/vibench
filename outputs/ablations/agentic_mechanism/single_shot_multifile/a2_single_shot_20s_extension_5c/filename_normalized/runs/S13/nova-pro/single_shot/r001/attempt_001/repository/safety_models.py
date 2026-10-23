from typing import Dict

class ModerationResponse:
    def __init__(self, categories: Dict[str, float], decision: str):
        self.categories = categories
        self.decision = decision

class RedactionResponse:
    def __init__(self, redacted_text: str):
        self.redacted_text = redacted_text