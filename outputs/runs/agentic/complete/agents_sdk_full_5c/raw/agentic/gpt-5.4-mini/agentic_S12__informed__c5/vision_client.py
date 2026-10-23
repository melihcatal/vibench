from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import boto3

from vision_models import ImageRequest, NormalizedVisionResult, clamp_text, normalize_labels, normalize_safety_findings, normalize_text_blocks


@dataclass
class VisionConfig:
    region_name: Optional[str] = None
    max_labels: int = 10
    language_code: str = "en"


def load_config() -> VisionConfig:
    return VisionConfig(
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        max_labels=int(os.getenv("VISION_MAX_LABELS", "10")),
        language_code=os.getenv("VISION_LANGUAGE_CODE", "en"),
    )


class VisionClient:
    def __init__(self, config: Optional[VisionConfig] = None):
        self.config = config or load_config()
        self._client = boto3.client("rekognition", region_name=self.config.region_name)

    @staticmethod
    def _image_bytes(image_path: str) -> bytes:
        with open(image_path, "rb") as f:
            return f.read()

    def detect_labels(self, req: ImageRequest) -> NormalizedVisionResult:
        response = self._client.detect_labels(
            Image={"Bytes": self._image_bytes(req.image_path)},
            MaxLabels=req.max_labels,
            MinConfidence=50.0,
        )
        labels = normalize_labels(response.get("Labels", []))
        return NormalizedVisionResult(labels=labels, raw=response)

    def detect_text(self, req: ImageRequest) -> NormalizedVisionResult:
        response = self._client.detect_text(Image={"Bytes": self._image_bytes(req.image_path)})
        text_blocks = normalize_text_blocks(response.get("TextDetections", []))
        return NormalizedVisionResult(text_blocks=text_blocks, raw=response)

    def describe_image(self, req: ImageRequest) -> NormalizedVisionResult:
        labels_resp = self._client.detect_labels(
            Image={"Bytes": self._image_bytes(req.image_path)},
            MaxLabels=req.max_labels,
            MinConfidence=50.0,
        )
        labels = normalize_labels(labels_resp.get("Labels", []))
        description = ", ".join(label.name for label in labels[:3])
        return NormalizedVisionResult(raw=labels_resp, labels=labels, description=None if not description else __import__("vision_models").VisionDescription(text=f"An image showing {description}.", confidence=labels[0].confidence if labels else None))

    def score_safety(self, req: ImageRequest) -> NormalizedVisionResult:
        response = self._client.detect_moderation_labels(Image={"Bytes": self._image_bytes(req.image_path)}, MinConfidence=50.0)
        findings = normalize_safety_findings(response.get("ModerationLabels", []))
        return NormalizedVisionResult(safety_findings=findings, raw=response)
