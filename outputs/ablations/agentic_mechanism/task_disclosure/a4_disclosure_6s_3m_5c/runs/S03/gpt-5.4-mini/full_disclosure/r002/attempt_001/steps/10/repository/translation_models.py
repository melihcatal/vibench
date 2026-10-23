from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_language(value: Any) -> Optional[str]:
    text = _normalize_text(value)
    return text or None


def _normalize_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def _normalize_metadata(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return dict(value)
    return {"value": value}


def _normalize_scores(value: Any) -> Dict[str, float]:
    if not isinstance(value, dict):
        return {}
    result: Dict[str, float] = {}
    for key, item in value.items():
        try:
            result[str(key)] = float(item)
        except (TypeError, ValueError):
            continue
    return result


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    model: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.text = _normalize_text(self.text)
        self.source_language = _normalize_language(self.source_language)
        self.target_language = _normalize_language(self.target_language)
        self.model = _normalize_text(self.model) or None
        self.metadata = _normalize_metadata(self.metadata)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"text": self.text}
        if self.source_language is not None:
            data["source_language"] = self.source_language
        if self.target_language is not None:
            data["target_language"] = self.target_language
        if self.model is not None:
            data["model"] = self.model
        if self.metadata:
            data["metadata"] = dict(self.metadata)
        return data


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    detected_language: Optional[str] = None
    model: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.translated_text = _normalize_text(self.translated_text)
        self.source_language = _normalize_language(self.source_language)
        self.target_language = _normalize_language(self.target_language)
        self.detected_language = _normalize_language(self.detected_language)
        self.model = _normalize_text(self.model) or None
        self.metadata = _normalize_metadata(self.metadata)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"translated_text": self.translated_text}
        if self.source_language is not None:
            data["source_language"] = self.source_language
        if self.target_language is not None:
            data["target_language"] = self.target_language
        if self.detected_language is not None:
            data["detected_language"] = self.detected_language
        if self.model is not None:
            data["model"] = self.model
        if self.metadata:
            data["metadata"] = dict(self.metadata)
        return data


@dataclass
class TranslationIssue:
    code: str
    message: str
    severity: str = "medium"
    details: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.code = _normalize_text(self.code)
        self.message = _normalize_text(self.message)
        self.severity = _normalize_text(self.severity) or "medium"
        self.details = _normalize_metadata(self.details)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "details": dict(self.details),
        }


@dataclass
class TranslationResponse:
    result: Union[TranslationResult, List[TranslationResult], None] = None
    issues: List[TranslationIssue] = field(default_factory=list)
    model: Optional[str] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if isinstance(self.result, dict):
            self.result = TranslationResult(**self.result)
        elif isinstance(self.result, list):
            self.result = [item if isinstance(item, TranslationResult) else TranslationResult(**item) for item in self.result]
        self.issues = [issue if isinstance(issue, TranslationIssue) else TranslationIssue(**issue) for issue in self.issues]
        self.model = _normalize_text(self.model) or None
        self.usage = _normalize_metadata(self.usage)
        self.metadata = _normalize_metadata(self.metadata)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "result": self._serialize_result(),
            "issues": [issue.to_dict() for issue in self.issues],
        }
        if self.model is not None:
            data["model"] = self.model
        if self.usage:
            data["usage"] = dict(self.usage)
        if self.metadata:
            data["metadata"] = dict(self.metadata)
        return data

    def _serialize_result(self) -> Any:
        if isinstance(self.result, list):
            return [item.to_dict() for item in self.result]
        if isinstance(self.result, TranslationResult):
            return self.result.to_dict()
        return None


def normalize_translation_request(data: Any) -> TranslationRequest:
    if isinstance(data, TranslationRequest):
        return data
    if isinstance(data, dict):
        return TranslationRequest(**data)
    return TranslationRequest(text=data)


def normalize_translation_response(data: Any) -> TranslationResponse:
    if isinstance(data, TranslationResponse):
        return data
    if isinstance(data, dict):
        return TranslationResponse(**data)
    return TranslationResponse(result=TranslationResult(translated_text=data))


def normalize_translation_text(data: Any) -> str:
    if isinstance(data, TranslationResult):
        return data.translated_text
    if isinstance(data, dict):
        if "translated_text" in data:
            return _normalize_text(data["translated_text"])
        if "text" in data:
            return _normalize_text(data["text"])
    return _normalize_text(data)


def is_successful_response(data: Any) -> bool:
    response = normalize_translation_response(data)
    return bool(response.result) and not response.issues


def extract_issues(data: Any) -> List[Dict[str, Any]]:
    response = normalize_translation_response(data)
    return [issue.to_dict() for issue in response.issues]


def merge_metadata(*parts: Any) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for part in parts:
        if isinstance(part, dict):
            merged.update(part)
    return merged
