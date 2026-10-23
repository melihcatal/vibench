import re
from dataclasses import dataclass, asdict
from typing import Any, Dict, List


def normalize_label_list(text: str) -> List[str]:
    parts = re.split(r"[\n,;•]+", text)
    cleaned = []
    seen = set()
    for part in parts:
        item = part.strip().lstrip("- ").strip()
        if not item:
            continue
        if item.lower() not in seen:
            seen.add(item.lower())
            cleaned.append(item)
    return cleaned


def normalize_text_lines(text: str) -> List[str]:
    lines = [line.strip() for line in text.splitlines()]
    return [line for line in lines if line]


def normalize_safety_label(text: str) -> str:
    lowered = text.lower()
    if any(token in lowered for token in ["unsafe", "high risk", "explicit", "violent", "hateful"]):
        return "unsafe"
    if any(token in lowered for token in ["low risk", "safe", "benign"]):
        return "safe"
    return "uncertain"


@dataclass
class LabelDetectionResult:
    labels: List[str]
    raw_text: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DescriptionResult:
    description: str
    raw_text: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class OCRResult:
    text: str
    lines: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SafetyResult:
    label: str
    rationale: str
    raw_text: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
