from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class VisionResult:
    provider: str
    data: Dict[str, Any] = field(default_factory=dict)


def normalize_labels(items: List[Dict[str, Any]]) -> List[str]:
    return [str(item.get("name", "")).strip() for item in items if item.get("name")]


def normalize_text(lines: List[Dict[str, Any]]) -> str:
    return " ".join(
        str(line.get("text", "")).strip() for line in lines if line.get("text")
    )


def normalize_safety(flags: Dict[str, Any]) -> Dict[str, Any]:
    return {
        k: flags.get(k) for k in ("adult", "racy", "gory", "violence") if k in flags
    }
