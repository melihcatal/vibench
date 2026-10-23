from typing import List, Dict, Any, Optional
from enum import Enum

class HarmCategory(str, Enum):
    TOXICITY = "TOXICITY"
    SEXUAL = "SEXUAL"
    VIOLENCE = "VIOLENCE"
    HARASSMENT = "HARASSMENT"
    HATE_SPEECH = "HATE_SPEECH"
    DANGEROUS_CONTENT = "DANGEROUS_CONTENT"

class ModerationScore:
    def __init__(self, category: HarmCategory, score: float):
        self.category = category
        self.score = score

class ModerationResult:
    def __init__(self, text: str, scores: List[ModerationScore], decision: str = "PENDING"):
        self.text = text
        self.scores = scores
        self.decision = decision

class BatchModerationRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts

class BatchModerationResponse:
    def __init__(self, results: List[ModerationResult]):
        self.results = results

class RedactionSpan:
    def __init__(self, start: int, end: int, original_text: str, redacted_text: str):
        self.start = start
        self.end = end
        self.original_text = original_text
        self.redacted_text = redacted_text

class RedactionResult:
    def __init__(self, original_text: str, redacted_text: str, spans: List[RedactionSpan]):
        self.original_text = original_text
        self.redacted_text = redacted_text
        self.spans = spans

class ModerationDecision:
    def __init__(self, text: str, decision: str, reason: Optional[str] = None):
        self.text = text
        self.decision = decision
        self.reason = reason