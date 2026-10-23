from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ImageAnalysisResult:
    provider: str
    kind: str
    text: str = ""
    items: List[str] = field(default_factory=list)
    score: Optional[float] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    def normalized_items(self) -> List[str]:
        return [str(item).strip() for item in self.items if str(item).strip()]


@dataclass
class VisualRequest:
    image_path: str
    prompt: Optional[str] = None
    language: Optional[str] = None


@dataclass
class ArchiveRecord:
    asset_key: str
    caption: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_label_items(items: Iterable[Any]) -> List[str]:
    return [str(item).strip() for item in items if str(item).strip()]


def join_short(items: Iterable[str], limit: int = 5) -> str:
    selected = [item for item in items if item]
    if not selected:
        return ""
    return ", ".join(selected[:limit])
