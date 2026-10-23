from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SafetyRequest:
    text: str
    language: str | None = None
    user_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_azure_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"text": self.text}
        if self.language:
            payload["language"] = self.language
        return payload


@dataclass(slots=True)
class CategoryScore:
    name: str
    severity: int


@dataclass(slots=True)
class SafetyResult:
    action: str
    categories: list[CategoryScore]
    provider: str
    raw: dict[str, Any]
    redacted_text: str | None = None

    def severity_map(self) -> dict[str, int]:
        return {item.name: item.severity for item in self.categories}


def normalize_categories(
    raw_categories: list[dict[str, Any]] | None,
) -> list[CategoryScore]:
    normalized: list[CategoryScore] = []
    for item in raw_categories or []:
        normalized.append(
            CategoryScore(
                name=str(item.get("category", "unknown")).lower(),
                severity=int(item.get("severity", 0)),
            )
        )
    return normalized


def normalize_action(severity_map: dict[str, int], thresholds: dict[str, int]) -> str:
    for category, severity in severity_map.items():
        if severity >= thresholds.get(category, 7):
            return "block"
    return "allow"


def summarize_decisions(results: list[SafetyResult]) -> dict[str, Any]:
    blocked = sum(1 for result in results if result.action != "allow")
    return {
        "total": len(results),
        "blocked": blocked,
        "allowed": len(results) - blocked,
        "providers": sorted({result.provider for result in results}),
    }
