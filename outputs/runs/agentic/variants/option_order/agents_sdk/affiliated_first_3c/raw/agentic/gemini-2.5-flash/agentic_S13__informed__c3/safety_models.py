from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class TextModerationRequest:
    """Represents a request for text moderation."""
    text: str
    language: str = "en"
    categories: List[str] = field(default_factory=list)
    return_redaction: bool = False

@dataclass
class TextModerationCategory:
    """Represents a moderation category and its score."""
    name: str
    score: float
    decision: Optional[str] = None # e.g., "accept", "reject", "review"

@dataclass
class TextModerationResult:
    """Represents the result of text moderation for a single piece of text."""
    original_text: str
    is_safe: bool
    categories: List[TextModerationCategory] = field(default_factory=list)
    redacted_text: Optional[str] = None
    provider_raw_response: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BatchModerationResult:
    """Represents the result of batch text moderation."""
    results: List[TextModerationResult]
    batch_summary: Dict[str, Any] = field(default_factory=dict)

def normalize_azure_content_safety_response(raw_response: dict, original_text: str) -> TextModerationResult:
    """Normalizes an Azure AI Content Safety response to TextModerationResult."""
    is_safe = True
    categories = []
    for category_result in raw_response.get("categories", []):
        category_name = category_result["category"]
        severity = category_result["severity"]
        score = severity / 4.0 # Assuming 4 severity levels are mapped to a 0-1 score
        
        decision = "accept"
        if severity > 0:
            is_safe = False
            if severity >= 2: # Example threshold for review/reject
                decision = "review" if severity < 4 else "reject"

        categories.append(TextModerationCategory(name=category_name, score=score, decision=decision))
    
    return TextModerationResult(
        original_text=original_text,
        is_safe=is_safe,
        categories=categories,
        provider_raw_response=raw_response
    )

def normalize_comprehend_toxicity_response(raw_response: dict, original_text: str) -> TextModerationResult:
    """Normalizes an Amazon Comprehend Toxicity response to TextModerationResult."""
    is_safe = True
    categories = []
    
    for score_item in raw_response.get("ToxicityScores", []):
        category_name = score_item["Name"]
        score = score_item["Score"]
        
        decision = "accept"
        if score > 0.5: # Example threshold
            is_safe = False
            decision = "reject" if score > 0.8 else "review"

        categories.append(TextModerationCategory(name=category_name, score=score, decision=decision))
    
    return TextModerationResult(
        original_text=original_text,
        is_safe=is_safe,
        categories=categories,
        provider_raw_response=raw_response
    )
