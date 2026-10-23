"""Local data models for safety operations."""
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class ModerationResult:
    """A standardized moderation result."""
    flagged: bool
    categories: Dict[str, bool]
    scores: Dict[str, float]
    details: Optional[str] = None

@dataclass
class RedactionResult:
    """A standardized redaction result."""
    redacted_text: str
    redactions_made: int

@dataclass
class ThresholdDecision:
    """A standardized decision based on category thresholds."""
    allow: bool
    reasons: List[str]

@dataclass
class ModerationDecision:
    """Represents a single moderation decision for summarization."""
    text_id: str
    decision: str # e.g., "allowed", "blocked"
    categories: List[str]
    rationale: str

@dataclass
class ModerationSummary:
    """Represents a summary of multiple moderation decisions."""
    total_reviews: int
    total_blocked: int
    category_counts: Dict[str, int]
    summary_text: str
