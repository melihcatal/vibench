from typing import Any, Dict, List

from vision_models import VisionResult


def image_summary(analysis: Dict[str, Any]) -> VisionResult:
    labels: List[Dict[str, Any]] = analysis.get("labels", [])
    text: List[Dict[str, Any]] = analysis.get("text", [])
    safety = analysis.get("safety", {})
    parts = []
    if labels:
        parts.append("labels: " + ", ".join(item.get("name", "") for item in labels[:3] if item.get("name")))
    if text:
        parts.append("text: " + ", ".join(item.get("text", "") for item in text[:2] if item.get("text")))
    if safety.get("unsafe"):
        parts.append("safety concerns detected")
    return VisionResult(provider="local.summary", kind="summary", source=str(analysis.get("source", "")), data={"summary": "; ".join(parts)})
