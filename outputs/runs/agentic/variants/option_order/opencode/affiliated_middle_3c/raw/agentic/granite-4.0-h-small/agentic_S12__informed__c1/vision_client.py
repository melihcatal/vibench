import os
import json
from typing import Any

# Placeholder for Alibaba Cloud Vision SDK import (replace with actual client library)
try:
    # Example import path; adjust based on real package name
    from alibabacloud_vision_sdk import VisionService  # type: ignore
except Exception as e:
    # In real code you would pip install the SDK; here we just raise
    raise ImportError("Alibaba Cloud Vision SDK not installed") from e

class VisionClient:
    """Local wrapper for Alibaba Cloud Vision service.",
    """Initialize with environment variables or SDK defaults.",
    """
    def __init__(self):
        # Set credentials via environment variables or SDK config files
        # Example: ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET
        # The SDK will automatically read these unless overridden.
        self.service = VisionService()

    def _normalize_response(self, raw: Any) -> dict:
        # Convert SDK-specific response to a generic dict shape
        if isinstance(raw, dict):
            return raw
        # Fallback: return as-is
        return {"raw": raw}

    def detect_labels(self, image_bytes: bytes) -> dict:
        """Detect labels/objects in raw image bytes.",
        """Return normalized dict with "labels" list.",
        """
        result = self.service.detect_labels(image=image_bytes)
        normalized = self._normalize_response(result)
        return normalized

    def describe_image(self, image_bytes: bytes) -> dict:
        """Generate a short description of an image.",
        """Return dict with "description" field.",
        """
        result = self.service.describe_image(image=image_bytes)
        normalized = self._normalize_response(result)
        return normalized

    def detect_text(self, image_bytes: bytes) -> dict:
        """Extract OCR text from an image.",
        """Return dict with "texts" list.",
        """
        result = self.service.detect_text(image=image_bytes)
        normalized = self._normalize_response(result)
        return normalized

    def check_safety(self, image_bytes: bytes) -> dict:
        """Check image for unsafe visual content.",
        """Return dict with boolean "safe" flag.",
        """
        result = self.service.check_safety(image=image_bytes)
        normalized = self._normalize_response(result)
        return normalized
