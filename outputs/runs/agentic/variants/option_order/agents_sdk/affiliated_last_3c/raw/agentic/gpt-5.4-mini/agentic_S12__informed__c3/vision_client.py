from __future__ import annotations

import base64
import os
from dataclasses import asdict
from typing import Any, Dict, List

from google.cloud import vision
from google.cloud import storage

from vision_models import (
    ArchivePayload,
    VisionDescription,
    VisionImageRequest,
    VisionLabel,
    VisionSafetyResult,
    VisionTextBlock,
    compact_description,
    normalize_labels,
    normalize_text_blocks,
)


class VisionConfig:
    def __init__(self) -> None:
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        self.bucket_name = os.getenv("VISION_ARCHIVE_BUCKET", "")


class GoogleVisionClient:
    def __init__(self, config: VisionConfig | None = None) -> None:
        self.config = config or VisionConfig()
        self.client = vision.ImageAnnotatorClient()

    def _image_from_path(self, path: str) -> vision.Image:
        with open(path, "rb") as fh:
            content = fh.read()
        return vision.Image(content=content)

    def detect_labels(self, request: VisionImageRequest) -> List[VisionLabel]:
        image = self._image_from_path(request.image_path)
        response = self.client.label_detection(image=image, max_results=request.max_results)
        items = [
            {"name": label.description, "confidence": label.score, "mid": label.mid}
            for label in response.label_annotations
        ]
        return normalize_labels(items)

    def describe_image(self, request: VisionImageRequest) -> VisionDescription:
        labels = self.detect_labels(request)
        text_blocks = self.detect_text(request)
        return VisionDescription(text=compact_description(labels, text_blocks), raw={"labels": [asdict(l) for l in labels]})

    def detect_text(self, request: VisionImageRequest) -> List[VisionTextBlock]:
        image = self._image_from_path(request.image_path)
        response = self.client.text_detection(image=image)
        blocks = [
            {"text": ann.description, "confidence": getattr(ann, "confidence", None), "locale": getattr(ann, "locale", None)}
            for ann in response.text_annotations[1:]
        ]
        if not blocks and response.text_annotations:
            blocks = [{"text": response.text_annotations[0].description, "confidence": None}]
        return normalize_text_blocks(blocks)

    def score_safety(self, request: VisionImageRequest) -> VisionSafetyResult:
        labels = self.detect_labels(request)
        risky = [label.name for label in labels if label.name.lower() in {"weapon", "violence", "adult", "blood"}]
        score = min(1.0, 0.25 * len(risky))
        return VisionSafetyResult(unsafe=bool(risky), score=score, categories=risky, raw={"labels": [asdict(l) for l in labels]})

    def archive_payload(self, object_key: str, metadata: Dict[str, Any], body: bytes) -> ArchivePayload:
        return ArchivePayload(object_key=object_key, metadata=metadata, body=body)


class GoogleStorageArchive:
    def __init__(self, bucket_name: str | None = None) -> None:
        self.client = storage.Client()
        self.bucket_name = bucket_name or os.getenv("VISION_ARCHIVE_BUCKET", "")

    def upload(self, payload: ArchivePayload) -> str:
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(payload.object_key)
        blob.metadata = {k: str(v) for k, v in payload.metadata.items()}
        blob.upload_from_string(payload.body)
        return f"gs://{self.bucket_name}/{payload.object_key}"


def image_to_base64(path: str) -> str:
    with open(path, "rb") as fh:
        return base64.b64encode(fh.read()).decode("utf-8")
