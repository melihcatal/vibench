from __future__ import annotations

import base64
import os
from dataclasses import asdict
from typing import Any, Dict, List, Optional

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from vision_models import (
    VisionDescription,
    VisionLabel,
    VisionRequest,
    VisionSafetyScore,
    VisionTextDetection,
    first_nonempty,
    normalize_confidence,
    normalize_text,
)

AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT", "")
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY", "")


class AzureVisionClient:
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        self.endpoint = endpoint or AZURE_VISION_ENDPOINT
        self.key = key or AZURE_VISION_KEY
        if not self.endpoint or not self.key:
            raise ValueError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY are required for Azure AI Vision")
        self._client = ImageAnalysisClient(self.endpoint, AzureKeyCredential(self.key))

    def _image_source(self, image_path: str) -> Any:
        with open(image_path, "rb") as handle:
            return handle.read()

    def analyze_labels(self, request: VisionRequest) -> List[VisionLabel]:
        result = self._client.analyze(
            image_data=self._image_source(request.image_path),
            visual_features=[VisualFeatures.OBJECTS, VisualFeatures.TAGS],
            language=request.language,
        )
        labels: List[VisionLabel] = []
        for item in getattr(result, "tags", [])[: request.max_results]:
            labels.append(
                VisionLabel(
                    name=normalize_text(getattr(item, "name", "")),
                    confidence=normalize_confidence(getattr(item, "confidence", None)) or 0.0,
                    extra={"raw": getattr(item, "as_dict", lambda: {})()},
                )
            )
        for obj in getattr(result, "objects", []):
            labels.append(
                VisionLabel(
                    name=normalize_text(getattr(obj, "name", "")),
                    confidence=normalize_confidence(getattr(obj, "confidence", None)) or 0.0,
                    extra={"box": getattr(obj, "bounding_box", None), "raw": getattr(obj, "as_dict", lambda: {})()},
                )
            )
        return labels[: request.max_results]

    def describe_image(self, request: VisionRequest) -> VisionDescription:
        result = self._client.analyze(
            image_data=self._image_source(request.image_path),
            visual_features=[VisualFeatures.CAPTION],
            language=request.language,
        )
        caption = getattr(result, "caption", None)
        if caption:
            return VisionDescription(
                text=first_nonempty(getattr(caption, "text", "")),
                confidence=normalize_confidence(getattr(caption, "confidence", None)),
                extra={"raw": getattr(caption, "as_dict", lambda: {})()},
            )
        return VisionDescription(text="")

    def detect_text(self, request: VisionRequest) -> List[VisionTextDetection]:
        result = self._client.analyze(
            image_data=self._image_source(request.image_path),
            visual_features=[VisualFeatures.READ],
            language=request.language,
        )
        detections: List[VisionTextDetection] = []
        for block in getattr(result, "read", []) or []:
            for line in getattr(block, "lines", []) or []:
                detections.append(
                    VisionTextDetection(
                        text=normalize_text(getattr(line, "text", "")),
                        confidence=normalize_confidence(getattr(line, "confidence", None)),
                        extra={"raw": getattr(line, "as_dict", lambda: {})()},
                    )
                )
        return detections

    def score_safety(self, request: VisionRequest) -> VisionSafetyScore:
        result = self._client.analyze(
            image_data=self._image_source(request.image_path),
            visual_features=[VisualFeatures.ADULT],
            language=request.language,
        )
        adult = getattr(result, "adult", None)
        category = "safe"
        severity = "low"
        confidence = None
        if adult:
            is_adult = any(bool(getattr(adult, field, False)) for field in ["is_adult_content", "is_gory_content", "is_racy_content"])
            if is_adult:
                category = "policy_sensitive"
                severity = "high"
            confidence = normalize_confidence(getattr(adult, "adult_score", None))
        return VisionSafetyScore(category=category, severity=severity, confidence=confidence, extra={"raw": getattr(adult, "as_dict", lambda: {})() if adult else {}})

    def analyze_all(self, request: VisionRequest) -> Dict[str, Any]:
        return {
            "labels": [asdict(item) for item in self.analyze_labels(request)],
            "description": asdict(self.describe_image(request)),
            "texts": [asdict(item) for item in self.detect_text(request)],
            "safety": asdict(self.score_safety(request)),
        }
