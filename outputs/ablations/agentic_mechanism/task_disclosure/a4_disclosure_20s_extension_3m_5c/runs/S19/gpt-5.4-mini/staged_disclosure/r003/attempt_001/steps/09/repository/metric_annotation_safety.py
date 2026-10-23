import os
import re
from dataclasses import dataclass
from typing import Dict, List, Optional

import boto3


_DEFAULT_BLOCKLIST = (
    r"\b(?:password|passwd|secret|token|api[_-]?key|access[_-]?key|private[_-]?key)\b",
    r"\b(?:drop\s+table|truncate\s+table|delete\s+from|insert\s+into|update\s+\w+\s+set)\b",
    r"[<>]{2,}|[`$]{2,}|\{\{|\}\}",
)


@dataclass(frozen=True)
class SafetyScanConfig:
    region_name: str = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
    comprehend_language_code: str = os.getenv("AWS_COMPREHEND_LANGUAGE_CODE", "en")
    max_length: int = int(os.getenv("METRIC_ANNOTATION_MAX_LENGTH", "512"))


@dataclass(frozen=True)
class SafetyFinding:
    label: str
    unsafe: bool
    reasons: List[str]


class MetricAnnotationSafetyChecker:
    def __init__(self, config: Optional[SafetyScanConfig] = None) -> None:
        self.config = config or SafetyScanConfig()
        self._comprehend = boto3.client("comprehend", region_name=self.config.region_name)

    def check_label(self, label: str) -> SafetyFinding:
        return self._check_text(label)

    def check_annotations(self, annotations: Dict[str, str]) -> Dict[str, SafetyFinding]:
        return {key: self._check_text(value) for key, value in annotations.items()}

    def is_safe(self, text: str) -> bool:
        return not self._check_text(text).unsafe

    def _check_text(self, text: str) -> SafetyFinding:
        normalized = (text or "").strip()
        reasons: List[str] = []

        if not normalized:
            reasons.append("empty_text")
        if len(normalized) > self.config.max_length:
            reasons.append("too_long")

        lowered = normalized.lower()
        for pattern in _DEFAULT_BLOCKLIST:
            if re.search(pattern, lowered, flags=re.IGNORECASE):
                reasons.append(f"matched_pattern:{pattern}")

        if normalized:
            try:
                language = self._comprehend.detect_dominant_language(Text=normalized).get("Languages", [])
                if language and language[0].get("LanguageCode") not in {self.config.comprehend_language_code, "und"}:
                    reasons.append("unexpected_language")
            except Exception:
                reasons.append("provider_check_unavailable")

        unsafe = bool(reasons)
        return SafetyFinding(label=normalized, unsafe=unsafe, reasons=reasons)
