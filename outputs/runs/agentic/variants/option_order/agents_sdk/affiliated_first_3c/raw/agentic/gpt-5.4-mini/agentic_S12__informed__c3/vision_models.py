from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class VisionRequest:
    image_path: str
    language: str = "en"
    prompt: Optional[str] = None
    max_results: int = 10


@dataclass
class VisionFinding:
    name: str
    confidence: float = 0.0
    text: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisionResponse:
    provider: str
    findings: List[VisionFinding] = field(default_factory=list)
    summary: Optional[str] = None
    unsafe: Optional[bool] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_label(name: str) -> str:
    return " ".join(name.strip().lower().replace("_", " ").split())


def coerce_findings(items: List[Dict[str, Any]]) -> List[VisionFinding]:
    findings: List[VisionFinding] = []
    for item in items:
        findings.append(
            VisionFinding(
                name=str(item.get("name") or item.get("label") or item.get("text") or ""),
                confidence=float(item.get("confidence") or item.get("score") or 0.0),
                text=item.get("text"),
                metadata={k: v for k, v in item.items() if k not in {"name", "label", "text", "confidence", "score"}},
            )
        )
    return findings
