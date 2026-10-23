from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, Optional, Union


class SafetyCategory(str, Enum):
    harassment = "harassment"
    hate = "hate"
    sexual = "sexual"
    violence = "violence"
    self_harm = "self_harm"
    spam = "spam"
    other = "other"


class SafetySeverity(str, Enum):
    safe = "safe"
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class SafetyAction(str, Enum):
    allow = "allow"
    warn = "warn"
    block = "block"
    review = "review"


@dataclass
class SafetyRequest:
    text: str
    categories: Optional[List[SafetyCategory]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"text": self.text}
        if self.categories is not None:
            payload["categories"] = [category.value if isinstance(category, SafetyCategory) else str(category) for category in self.categories]
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass
class SafetyFinding:
    category: SafetyCategory
    severity: SafetySeverity
    action: SafetyAction
    confidence: float = 0.0
    explanation: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SafetyFinding":
        return cls(
            category=SafetyCategory(str(data.get("category", SafetyCategory.other.value))),
            severity=SafetySeverity(str(data.get("severity", SafetySeverity.safe.value))),
            action=SafetyAction(str(data.get("action", SafetyAction.allow.value))),
            confidence=float(data.get("confidence", 0.0) or 0.0),
            explanation=str(data.get("explanation", "") or ""),
        )


@dataclass
class SafetyResponse:
    safe: bool
    action: SafetyAction
    findings: List[SafetyFinding] = field(default_factory=list)
    normalized_text: str = ""
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SafetyResponse":
        findings_data = data.get("findings", [])
        findings = [SafetyFinding.from_dict(item) for item in findings_data if isinstance(item, Mapping)]
        return cls(
            safe=bool(data.get("safe", True)),
            action=SafetyAction(str(data.get("action", SafetyAction.allow.value))),
            findings=findings,
            normalized_text=str(data.get("normalized_text", "") or ""),
            raw=dict(data),
        )


def normalize_text_content(text: str) -> str:
    if text is None:
        return ""
    normalized = " ".join(str(text).split())
    return normalized.strip()


def normalize_request(request: Union[SafetyRequest, Mapping[str, Any], str]) -> SafetyRequest:
    if isinstance(request, SafetyRequest):
        return request
    if isinstance(request, str):
        return SafetyRequest(text=normalize_text_content(request))
    text = normalize_text_content(str(request.get("text", "")))
    categories = request.get("categories")
    normalized_categories: Optional[List[SafetyCategory]] = None
    if categories is not None:
        normalized_categories = [SafetyCategory(str(item)) for item in categories]
    metadata = dict(request.get("metadata", {}) or {})
    return SafetyRequest(text=text, categories=normalized_categories, metadata=metadata)


def normalize_response(response: Union[SafetyResponse, Mapping[str, Any]]) -> SafetyResponse:
    if isinstance(response, SafetyResponse):
        return response
    normalized = dict(response)
    normalized["normalized_text"] = normalize_text_content(str(normalized.get("normalized_text", normalized.get("text", ""))))
    return SafetyResponse.from_dict(normalized)


def summarize_findings(findings: Iterable[SafetyFinding]) -> Dict[str, int]:
    summary: Dict[str, int] = {}
    for finding in findings:
        key = finding.category.value
        summary[key] = summary.get(key, 0) + 1
    return summary
