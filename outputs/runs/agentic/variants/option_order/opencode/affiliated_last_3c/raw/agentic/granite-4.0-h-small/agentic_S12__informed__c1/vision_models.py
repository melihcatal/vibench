from __future__ import annotations
from dataclasses import dataclass
from typing import List, Mapping, Optional

# Normalized response models that each same‑scenario function returns


def _list_or_empty(seq: Optional[List[Mapping]]) -> List[Mapping]:
    return seq if seq is not None else []


@dataclass
class LabelsResponse:
    labels: List[Mapping]  # name, confidence, etc.
    provider: str = "DashScope"

    @classmethod
    def from_dashscope(cls, raw: dict) -> LabelsResponse:
        return cls(labels=raw.get("labels", []))


@dataclass
class DescriptionResponse:
    text: str
    provider: str = "DashScope"

    @classmethod
    def from_dashscope(cls, raw: dict) -> DescriptionResponse:
        return cls(text=raw.get("description", ""))


@dataclass
class TextDetectionResponse:
    extracted_text: str
    provider: str = "DashScope"

    @classmethod
    def from_dashscope(cls, raw: dict) -> TextDetectionResponse:
        return cls(extracted_text=raw.get("text", ""))


@dataclass
class SafetyCheckResponse:
    safe: bool
    unsafe_categories: List[str]
    provider: str = "DashScope"

    @classmethod
    def from_dashscope(cls, raw: dict) -> SafetyCheckResponse:
        return cls(
            safe=raw.get("is_safe", True),
            unsafe_categories=raw.get("unsafe_categories", []),
        )
