# [HELPER] safety_models.py

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

# Models representing request payloads and responses for the safety service.

@dataclass
class Span:
    start: int
    end: int
    category: str

@dataclass
class SafetyRequest:
    text: str
    categories: Optional[List[str]] = None

@dataclass
class SafetyResponse:
    unsafe_spans: List[Span]
    category_scores: Dict[str, float]
    overall_verdict: str  # 'safe' or 'unsafe'

@dataclass
class SafetyRequestBatch:
    inputs: List[SafetyRequest]

@dataclass
class SafetyResponseBatch:
    results: List[SafetyResponse]

# Normalization helper to flatten results for downstream steps.
def normalize_response(response: Any) -> SafetyResponse:
    """Convert provider‑specific response into our canonical SafetyResponse."""
    # Placeholder conversion logic.
    unsafe_spans = []
    category_scores = {}
    overall_verdict = "safe"
    # Example: if response has fields named differently, map them here.
    return SafetyResponse(unsafe_spans=unsafe_spans,
                          category_scores=category_scores,
                          overall_verdict=overall_verdict)
