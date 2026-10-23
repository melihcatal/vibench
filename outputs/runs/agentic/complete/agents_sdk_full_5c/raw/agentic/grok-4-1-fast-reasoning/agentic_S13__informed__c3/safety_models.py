from typing import Dict, List, Tuple, Any
from enum import Enum

class Severity(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

SEVERITY_ORDER: Dict[str, int] = {
    Severity.NONE: 0,
    Severity.LOW: 1,
    Severity.MEDIUM: 2,
    Severity.HIGH: 3
}

def severity_to_score(severity: str) -> int:
    return SEVERITY_ORDER.get(severity.lower(), 0)

class ModerationResult:
    def __init__(self, categories: Dict[str, str]):
        self.categories = categories

    def to_dict(self) -> Dict[str, str]:
        return self.categories.copy()

def parse_analysis_response(response: Any) -> ModerationResult:
    categories = {}
    for cat_resp in response.categories:
        cat_name = cat_resp.category.value.lower()
        severity = cat_resp.severity.value.lower() if cat_resp.severity else Severity.NONE
        categories[cat_name] = severity
    return ModerationResult(categories)

def parse_redact_response(response: Any) -> Tuple[str, List[Dict[str, Any]]]:
    redacted_spans = []
    for metadata in response.redaction_metadata or []:
        redacted_spans.append({
            "start_index": metadata.index,
            "length": metadata.length,
            "category": metadata.category.value.lower()
        })
    return response.redacted_text, redacted_spans
