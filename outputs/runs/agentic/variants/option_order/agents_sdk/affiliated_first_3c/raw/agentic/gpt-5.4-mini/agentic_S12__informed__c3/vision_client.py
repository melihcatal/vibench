from __future__ import annotations

import base64
import os
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis.models import VisualFeatures

from vision_models import VisionFinding, VisionRequest, VisionResponse, coerce_findings

AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT", "")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY", "")


def load_image_bytes(image_path: str) -> bytes:
    return Path(image_path).read_bytes()


def image_as_data_url(image_path: str) -> str:
    raw = load_image_bytes(image_path)
    encoded = base64.b64encode(raw).decode("ascii")
    suffix = Path(image_path).suffix.lower().lstrip(".") or "jpeg"
    mime = "image/jpeg" if suffix in {"jpg", "jpeg"} else f"image/{suffix}"
    return f"data:{mime};base64,{encoded}"


def azure_client() -> ImageAnalysisClient:
    if not AZURE_VISION_ENDPOINT or not AZURE_VISION_KEY:
        raise EnvironmentError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY are required")
    return ImageAnalysisClient(endpoint=AZURE_VISION_ENDPOINT, credential=AzureKeyCredential(AZURE_VISION_KEY))


def analyze_image(request: VisionRequest, features: List[str]) -> VisionResponse:
    client = azure_client()
    visual_features = [getattr(VisualFeatures, feature) for feature in features]
    result = client.analyze_from_file(load_image_bytes(request.image_path), visual_features=visual_features)
    raw: Dict[str, Any] = result.as_dict() if hasattr(result, "as_dict") else {}
    findings: List[VisionFinding] = []
    if getattr(result, "objects", None):
        findings.extend(
            VisionFinding(name=obj.name, confidence=float(obj.confidence or 0.0), metadata={"box": asdict(obj.bounding_box) if getattr(obj, "bounding_box", None) else None})
            for obj in result.objects.values
        )
    if getattr(result, "read", None) and getattr(result.read, "blocks", None):
        for block in result.read.blocks:
            for line in getattr(block, "lines", []):
                findings.append(VisionFinding(name="text", confidence=1.0, text=line.text))
    summary = None
    if getattr(result, "caption", None):
        summary = result.caption.text
    return VisionResponse(provider="Azure AI Vision", findings=findings, summary=summary, raw=raw)
