from typing import List, Literal, Dict, Any


class TextModerationRequest:
    def __init__(self, text: str):
        self.text = text


class TextModerationResponse:
    def __init__(
        self, categories_analysis: Dict[str, Any], block_id: str | None = None
    ):
        self.categories_analysis = categories_analysis
        self.block_id = block_id


class TextRedactionRequest:
    def __init__(self, text: str):
        self.text = text


class TextRedactionResponse:
    def __init__(self, redacted_text: str):
        self.redacted_text = redacted_text


class ModerationDecision:
    def __init__(self, text: str, is_safe: bool, categories_scores: Dict[str, float]):
        self.text = text
        self.is_safe = is_safe
        self.categories_scores = categories_scores


class ThresholdConfig:
    def __init__(self, category: str, threshold: float):
        self.category = category
        self.threshold = threshold
