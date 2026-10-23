import os
from typing import Optional

from google.cloud import vision

from vision_models import VisionImageInput, VisionResult, normalize_strings


class VisionClient:
    def __init__(self, client: Optional[vision.ImageAnnotatorClient] = None):
        self.client = client or vision.ImageAnnotatorClient()

    @classmethod
    def from_env(cls) -> "VisionClient":
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            return cls()
        return cls()

    def _load_image(self, image: VisionImageInput) -> vision.Image:
        if image.image_bytes is not None:
            return vision.Image(content=image.image_bytes)
        if image.image_path:
            with open(image.image_path, "rb") as f:
                return vision.Image(content=f.read())
        raise ValueError("image_path or image_bytes is required")

    def detect_labels(self, image: VisionImageInput) -> VisionResult:
        response = self.client.label_detection(image=self._load_image(image))
        labels = normalize_strings([ann.description for ann in response.label_annotations])
        return VisionResult(labels=labels, raw=response)

    def describe_image(self, image: VisionImageInput) -> VisionResult:
        response = self.client.image_annotation(image=self._load_image(image), features=[{"type_": vision.Feature.Type.LABEL_DETECTION}])
        labels = normalize_strings([ann.description for ann in response.label_annotations])
        desc = labels[0] if labels else ""
        return VisionResult(description=desc, labels=labels, raw=response)

    def detect_text(self, image: VisionImageInput) -> VisionResult:
        response = self.client.text_detection(image=self._load_image(image))
        text = normalize_strings([ann.description for ann in response.text_annotations[1:]])
        return VisionResult(text=text, raw=response)

    def score_safety(self, image: VisionImageInput) -> VisionResult:
        response = self.client.safe_search_detection(image=self._load_image(image))
        safety = {
            "adult": str(response.safe_search_annotation.adult),
            "spoof": str(response.safe_search_annotation.spoof),
            "medical": str(response.safe_search_annotation.medical),
            "violence": str(response.safe_search_annotation.violence),
            "racy": str(response.safe_search_annotation.racy),
        }
        return VisionResult(safety=safety, raw=response)
