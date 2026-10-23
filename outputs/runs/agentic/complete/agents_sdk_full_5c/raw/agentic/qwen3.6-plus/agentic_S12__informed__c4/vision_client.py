"""
vision_client.py - Provide local configuration and client helper utilities
for Static Image and Visual Understanding using Google Cloud Vision.

Handles credential setup, client initialization, image encoding, and
common request-building utilities shared across vision analysis tasks.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional, Tuple

from google.cloud import vision_v1
from google.cloud.vision_v1 import enums as vision_enums
from google.oauth2 import service_account


class VisionClientManager:
    """Manages lifecycle and configuration of Google Cloud Vision client."""

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        project_id: Optional[str] = None,
    ) -> None:
        self._client: Optional[vision_v1.ImageAnnotatorClient] = None
        self._credentials_path = credentials_path or os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )
        self._project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")

    def get_client(self) -> vision_v1.ImageAnnotatorClient:
        """Return a cached or newly created ImageAnnotatorClient."""
        if self._client is not None:
            return self._client

        if self._credentials_path and os.path.isfile(self._credentials_path):
            credentials = service_account.Credentials.from_service_account_file(
                self._credentials_path
            )
            self._client = vision_v1.ImageAnnotatorClient(credentials=credentials)
        else:
            self._client = vision_v1.ImageAnnotatorClient()
        return self._client

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None


def build_image_source(image_bytes: bytes) -> vision_v1.Image:
    """Build a google.cloud.vision_v1.Image from raw bytes."""
    image = vision_v1.Image()
    image.content = image_bytes
    return image


def build_image_source_from_url(url: str) -> vision_v1.Image:
    """Build a google.cloud.vision_v1.Image from a public URL."""
    image = vision_v1.Image()
    image.source.image_uri = url
    return image


def build_label_detection_config(
    max_results: int = 10,
) -> vision_v1.Feature:
    """Build a LABEL_DETECTION feature config."""
    feature = vision_v1.Feature()
    feature.type_ = vision_enums.Feature.Type.LABEL_DETECTION
    feature.max_results = max_results
    return feature


def build_text_detection_config(
    max_results: int = 50,
) -> vision_v1.Feature:
    """Build a TEXT_DETECTION feature config."""
    feature = vision_v1.Feature()
    feature.type_ = vision_enums.Feature.Type.TEXT_DETECTION
    feature.max_results = max_results
    return feature


def build_safe_search_config() -> vision_v1.Feature:
    """Build a SAFE_SEARCH_DETECTION feature config."""
    feature = vision_v1.Feature()
    feature.type_ = vision_enums.Feature.Type.SAFE_SEARCH_DETECTION
    return feature


def build_image_context(
    language_hints: Optional[list[str]] = None,
) -> vision_v1.ImageContext:
    """Build ImageContext with optional language hints for OCR."""
    context = vision_v1.ImageContext()
    if language_hints:
        context.language_hints = language_hints
    return context


def build_annotated_request(
    image: vision_v1.Image,
    features: list[vision_v1.Feature],
    context: Optional[vision_v1.ImageContext] = None,
) -> vision_v1.AnnotateImageRequest:
    """Build a complete AnnotateImageRequest."""
    request = vision_v1.AnnotateImageRequest()
    request.image = image
    request.features = features
    if context is not None:
        request.image_context = context
    return request


def fetch_image_as_bytes(image_url: str) -> bytes:
    """Download an image from a URL and return its bytes."""
    import urllib.request

    with urllib.request.urlopen(image_url) as response:
        return response.read()
