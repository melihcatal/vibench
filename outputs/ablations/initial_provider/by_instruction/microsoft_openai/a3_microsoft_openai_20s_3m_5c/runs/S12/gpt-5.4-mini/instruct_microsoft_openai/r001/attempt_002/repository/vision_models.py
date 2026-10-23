from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


def normalize_labels(text: str) -> List[str]:
    items = []
    for part in text.replace("\n", ",").split(","):
        label = part.strip().strip("-•*")
        if label:
            items.append(label)
    return items


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


@dataclass
class ImageAnalysisResult:
    content: str
    labels: Optional[List[str]] = None
    unsafe: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return {k: v for k, v in data.items() if v is not None}
