from typing import List, Dict, Any


class TextModerationRequest:
    def __init__(self, text: str):
        self.text = text


class TextModerationBatchRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts


class TextModerationResult:
    def __init__(self, categories_analysis: List[Dict[str, Any]]):
        self.categories_analysis = categories_analysis

    def is_unsafe(self, category: str, threshold: float) -> bool:
        for analysis in self.categories_analysis:
            if (
                analysis.get("category") == category
                and analysis.get("severity", 0) >= threshold
            ):
                return True
        return False


class RedactionResult:
    def __init__(
        self, original_text: str, redacted_text: str, blocks: List[Dict[str, Any]]
    ):
        self.original_text = original_text
        self.redacted_text = redacted_text
        self.blocks = blocks
