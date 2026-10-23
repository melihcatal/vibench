import base64
import os
from typing import Any, Dict, Optional

import boto3

from vision_models import ImageAnalysisRequest


class VisionClient:
    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
        self._client = boto3.client("rekognition", region_name=self.region_name)

    def _read_bytes(self, request: ImageAnalysisRequest) -> bytes:
        if request.image_bytes is not None:
            return request.image_bytes
        with open(request.image_path, "rb") as f:
            return f.read()

    def _image(self, request: ImageAnalysisRequest) -> Dict[str, Any]:
        return {"Bytes": self._read_bytes(request)}

    def detect_labels(self, request: ImageAnalysisRequest, max_labels: int = 20, min_confidence: float = 70.0) -> Dict[str, Any]:
        return self._client.detect_labels(Image=self._image(request), MaxLabels=max_labels, MinConfidence=min_confidence)

    def detect_text(self, request: ImageAnalysisRequest) -> Dict[str, Any]:
        return self._client.detect_text(Image=self._image(request))

    def detect_moderation_labels(self, request: ImageAnalysisRequest) -> Dict[str, Any]:
        return self._client.detect_moderation_labels(Image=self._image(request))

    def describe_image(self, request: ImageAnalysisRequest, max_labels: int = 5) -> str:
        payload = self.detect_labels(request, max_labels=max_labels)
        labels = [item.get("Name") for item in payload.get("Labels", []) if item.get("Name")]
        return ", ".join(labels[:max_labels])

    def encode_image_b64(self, request: ImageAnalysisRequest) -> str:
        return base64.b64encode(self._read_bytes(request)).decode("ascii")
