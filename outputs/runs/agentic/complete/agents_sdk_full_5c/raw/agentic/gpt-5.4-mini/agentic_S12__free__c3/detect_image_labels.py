from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from vision_client import get_computer_vision_client, read_image_bytes
from vision_models import LabelDetectionResult, normalize_label_items


def detect_image_labels(image_path: str | Path, max_labels: int = 20) -> LabelDetectionResult:
    """Detect labels/objects in a static image using Azure AI Vision."""
    client = get_computer_vision_client()
    image_bytes = read_image_bytes(image_path)
    result = client.analyze(
        image_data=image_bytes,
        visual_features=["tags"],
    )

    tags: List[Dict[str, Any]] = []
    for tag in getattr(result, "tags", []) or []:
        tags.append({"name": getattr(tag, "name", None), "confidence": getattr(tag, "confidence", None)})

    labels = normalize_label_items(tags)[:max_labels]
    return LabelDetectionResult(labels=labels, raw=result)
