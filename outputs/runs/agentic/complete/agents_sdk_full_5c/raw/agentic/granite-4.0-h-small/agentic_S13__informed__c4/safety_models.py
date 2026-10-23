from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

class Category:
    HARASSMENT = 'harassment'
    SELF_HARM = 'self_harm'
    HATE_SPEECH = 'hate_speech'
    SEXUAL_CONTENT = 'sexual_content'
    # Add more as needed

@dataclass(frozen=True)
class CategoryScore:
    """Score from a particular provider for a specific category."""
    category: str
    score: float  # 0.0 to 1.0 confidence

class UnsafeSpan:
    def __init__(self, start: int, end: int, category: str = None):
        self.start = start
        self.end = end
        self.category = category  # e.g., 'hate_speech', 'self_harm'
    def __repr__(self):
        return f"UnsafeSpan(start={self.start}, end={self.end}, category={self.category})"

class ModerationRequest:
    def __init__(self, text: str):
        self.text = text
    def __repr__(self):
        return f"ModerationRequest(text='{self.text[:20]}...')"

class ModerationResponse:
    def __init__(self, request: ModerationRequest, categories: List[CategoryScore], raw: Optional[dict] = None):
        self.request = request
        self.categories = categories
        self.raw = raw
    def __repr__(self):
        return f"ModerationResponse(request={self.request}, categories={self.categories})"

# NormalizedScore wraps the boolean decision and the original confidence
NormalizedScore = Tuple[bool, float]
