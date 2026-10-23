from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ImageSource:
    path: Optional[str] = None
    bucket: Optional[str] = None
    key: Optional[str] = None
    bytes_data: Optional[bytes] = None


def normalize_text_list(items: Any) -> List[str]:
    if not items:
        return []
    out = []
    for item in items:
        if isinstance(item, str):
            out.append(item)
        elif isinstance(item, dict):
            for k in ("Name", "name", "Text", "text", "Label", "label"):
                if k in item and item[k]:
                    out.append(str(item[k]))
                    break
    return out


def normalize_detect_labels_response(resp: Dict[str, Any]) -> Dict[str, Any]:
    labels = []
    for label in resp.get("Labels", []):
        labels.append({
            "name": label.get("Name"),
            "confidence": float(label.get("Confidence", 0.0)),
            "parents": normalize_text_list(label.get("Parents", [])),
            "categories": normalize_text_list(label.get("Categories", [])),
        })
    return {"labels": labels}


def normalize_text_detection_response(resp: Dict[str, Any]) -> Dict[str, Any]:
    blocks = []
    for block in resp.get("TextDetections", []):
        blocks.append({
            "text": block.get("DetectedText"),
            "type": block.get("Type"),
            "confidence": float(block.get("Confidence", 0.0)),
        })
    return {"text": blocks}


def normalize_safety_response(resp: Dict[str, Any]) -> Dict[str, Any]:
    labels = []
    for label in resp.get("Labels", []):
        labels.append({
            "name": label.get("Name"),
            "confidence": float(label.get("Confidence", 0.0)),
        })
    return {"unsafe_labels": labels}
