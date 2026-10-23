from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class ModerationCategory:
    """Represents a single moderation category with its score/severity."""
    name: str
    severity: int # e.g., 0-4 for Azure, or other scoring

@dataclass
class TextModerationResult:
    """Standardized result for text moderation."""
    text: str
    categories: List[ModerationCategory] = field(default_factory=list)
    overall_decision: Optional[str] = None # e.g., "Allow", "Flag", "Block"
    raw_response: Optional[Dict[str, Any]] = None

def normalize_azure_content_safety_response(text: str, azure_response: Dict[str, Any]) -> TextModerationResult:
    """Normalizes Azure AI Content Safety response to a common format."""
    categories = []
    for cat_analysis in azure_response.get("categories_analysis", []):
        categories.append(ModerationCategory(
            name=cat_analysis.get("category", "unknown"),
            severity=cat_analysis.get("severity", 0)
        ))
    
    # Determine a simple overall decision based on severities
    overall_decision = "Allow"
    if any(c.severity > 0 for c in categories):
        overall_decision = "Flag"
    if any(c.severity >= 4 for c in categories): # Assuming severity 4 is high
        overall_decision = "Block"

    return TextModerationResult(
        text=text,
        categories=categories,
        overall_decision=overall_decision,
        raw_response=azure_response
    )

def normalize_tisane_response(text: str, tisane_response: Dict[str, Any]) -> TextModerationResult:
    """Normalizes Tisane API response to a common format."""
    categories = []
    # Tisane response structure can be complex, this is a simplified example.
    # It often returns "violations" or "sentiment" data.
    if "violations" in tisane_response:
        for violation in tisane_response["violations"]:
            categories.append(ModerationCategory(
                name=violation.get("type", "unknown_violation"),
                severity=1 # Tisane typically gives presence, not severity levels like 0-4
            ))
            if "tags" in violation:
                for tag in violation["tags"]:
                    categories.append(ModerationCategory(name=tag, severity=1))
    
    overall_decision = "Allow"
    if categories:
        overall_decision = "Flag"

    return TextModerationResult(
        text=text,
        categories=categories,
        overall_decision=overall_decision,
        raw_response=tisane_response
    )
