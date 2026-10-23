from typing import Dict, Any, List
import os

class Violation(Dict[str, Any]):
    label: str
    confidence: float
    evidence: List[Dict[str, Any]]

DEFAULT_THRESHOLDS: Dict[str, float] = {
    "Profanity": 0.6,
    "Drugs": 0.8,
    "Violence": 0.8,
    "Sexually explicit": 0.8,
    "Hate speech": 0.8,
    "Bullying &amp; Harassment": 0.8,
    "Self-harm": 0.9
}

def get_default_thresholds() -&gt; Dict[str, float]:
    return DEFAULT_THRESHOLDS.copy()