from typing import List, Dict, Any, Optional
from enum import Enum

class ModerationCategory(str, Enum):
    TOXICITY = "TOXICITY"
    # Add other categories as needed, e.g., SEXUAL, HATE, VIOLENCE

class ModerationResult:
    def __init__(self, category: ModerationCategory, score: float, unsafe: bool = False):
        self.category = category
        self.score = score
        self.unsafe = unsafe

class TextModerationRequest:
    def __init__(self, text: str, language_code: str = "en"):
        self.text = text
        self.language_code = language_code

class TextModerationResponse:
    def __init__(self, results: List[ModerationResult]):
        self.results = results

class BatchTextModerationRequest:
    def __init__(self, texts: List[str], language_code: str = "en"):
        self.texts = texts
        self.language_code = language_code

class BatchTextModerationResponse:
    def __init__(self, batch_results: List[TextModerationResponse]):
        self.batch_results = batch_results

class RedactionSpan:
    def __init__(self, start: int, end: int, category: ModerationCategory, original_text: str):
        self.start = start
        self.end = end
        self.category = category
        self.original_text = original_text

class RedactionResponse:
    def __init__(self, redacted_text: str, spans: List[RedactionSpan]):
        self.redacted_text = redacted_text
        self.spans = spans
