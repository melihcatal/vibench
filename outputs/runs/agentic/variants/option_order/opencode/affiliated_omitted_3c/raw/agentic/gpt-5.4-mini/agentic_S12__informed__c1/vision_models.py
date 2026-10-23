from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class VisionRequest:
    image_url: str
    prompt: str = ""
    language: str = "en"


@dataclass
class VisionResult:
    text: str
    labels: List[str]
    unsafe: bool
    metadata: Dict[str, Any]


def normalize_labels(items: Optional[List[Any]]) -> List[str]:
    if not items:
        return []
    out = []
    for item in items:
        if isinstance(item, str):
            out.append(item.strip())
        elif isinstance(item, dict):
            value = item.get("label") or item.get("name") or item.get("text")
            if value:
                out.append(str(value).strip())
    return [x for x in out if x]


def make_result(
    text: str = "",
    labels: Optional[List[Any]] = None,
    unsafe: bool = False,
    **metadata: Any,
) -> VisionResult:
    return VisionResult(
        text=text, labels=normalize_labels(labels), unsafe=unsafe, metadata=metadata
    )
