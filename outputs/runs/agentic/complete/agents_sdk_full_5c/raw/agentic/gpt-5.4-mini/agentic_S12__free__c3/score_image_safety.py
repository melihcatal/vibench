from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

from vision_client import get_azure_vision_client, read_image_bytes
from vision_models import SafetyScoreResult, normalize_safety_score


def score_image_safety(image_path: str | Path) -> SafetyScoreResult:
    """Check unsafe/policy-sensitive visual content using Azure AI Content Safety."""
    client = get_azure_vision_client()
    image_bytes = read_image_bytes(image_path)
    analysis = client.analyze_image(
        image_bytes=image_bytes,
        categories=["violence", "self_harm", "nudity"],
    )
    data: Dict[str, Any] = getattr(analysis, "model_dump", lambda: {})() or {}
    score = normalize_safety_score(data)
    return SafetyScoreResult(score=score, raw=analysis)
