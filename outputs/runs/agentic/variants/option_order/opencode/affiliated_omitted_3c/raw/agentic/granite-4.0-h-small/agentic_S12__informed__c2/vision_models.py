import os

# ---------------------------------------------------------------------------
# Helper: Common request / response models for Static Image & Visual Understanding
# ---------------------------------------------------------------------------


class ImageRequest:
    """Placeholder for a unified request object used by provider wrappers."""

    def __init__(self, image_bytes: bytes):
        self.image = image_bytes
        self.features = []  # e.g., ["Labels", "Description", "Ocr"]

    def add_feature(self, feature: str):
        self.features.append(feature)


class ImageResponse:
    """Unified container for responses from different providers."""

    def __init__(self):
        self.labels = []  # list of label names or objects
        self.description = ""  # free‑form caption
        self.ocr_lines = []  # list of line objects from OCR
        self.safe = True  # safety check result

    def merge(self, other):
        self.labels.extend(other.labels)
        self.description = other.description or self.description
        self.ocr_lines.extend(other.ocr_lines)
        self.safe = self.safe and other.safe


class ImageAnalysis:
    """
    Helper to hold the full analysis result after calling multiple same‑scenario functions.
    """

    def __init__(self):
        self.labels = []
        self.description = ""
        self.ocr = []
        self.safe = True

    def add(self, request: ImageRequest, response: ImageResponse):
        self.labels.extend(response.labels)
        if response.description:
            self.description = response.description
        self.ocr.extend(response.ocr_lines)
        self.safe = self.safe and response.safe

    def to_dict(self):
        return {
            "labels": self.labels,
            "description": self.description,
            "ocr": [line.text for line in self.ocr],
            "safe": self.safe,
        }
