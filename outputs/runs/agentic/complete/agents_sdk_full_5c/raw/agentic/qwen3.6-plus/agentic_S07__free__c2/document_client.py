"""
Local configuration and client helper utilities for OCR and Layout Extraction.
Provides shared client initialization, credential loading, and helper methods
for Google Cloud Vision API interactions.
"""

import os
import base64
from typing import Optional, Dict, Any
from google.cloud import vision_v1
from google.api_core import client_options


GOOGLE_CLOUD_VISION_ENDPOINT = "vision.googleapis.com"
GOOGLE_CLOUD_DOCUMENT_AI_ENDPOINT = "documentai.googleapis.com"

# Provider-specific environment variables
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "ocr-layout-extraction-project")


class GoogleVisionClient:
    """Client wrapper for Google Cloud Vision API OCR and document analysis."""

    def __init__(self, credentials_path: Optional[str] = None, project: Optional[str] = None):
        self.credentials_path = credentials_path or GOOGLE_APPLICATION_CREDENTIALS
        self.project = project or GOOGLE_CLOUD_PROJECT
        
        client_options_config = client_options.ClientOptions(
            api_endpoint=GOOGLE_CLOUD_VISION_ENDPOINT
        )
        
        if self.credentials_path and os.path.exists(self.credentials_path):
            from google.oauth2 import service_account
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path
            )
            self.client = vision_v1.ImageAnnotatorClient(
                credentials=credentials,
                client_options=client_options_config
            )
        else:
            self.client = vision_v1.ImageAnnotatorClient(
                client_options=client_options_config
            )

    def encode_image_to_base64(self, image_path: str) -> bytes:
        """Encode a local image file to base64 bytes for Google Vision API."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read())

    def create_image_object(self, image_content: bytes) -> vision_v1.Image:
        """Create a Google Vision API Image object from bytes."""
        image = vision_v1.Image()
        image.content = image_content
        return image

    def create_feature(self, feature_type: str, max_results: int = 1) -> vision_v1.Feature:
        """Create a Google Vision API Feature object."""
        feature = vision_v1.Feature()
        feature.type_ = getattr(vision_v1.Feature.Type, feature_type)
        feature.max_results = max_results
        return feature

    def build_annotation_request(
        self,
        image_content: bytes,
        features: list,
        image_context: Optional[Dict[str, Any]] = None
    ) -> vision_v1.AnnotateImageRequest:
        """Build a complete Google Vision API annotation request."""
        image = self.create_image_object(image_content)
        
        request = vision_v1.AnnotateImageRequest()
        request.image = image
        request.features = features
        
        if image_context:
            request.image_context = vision_v1.ImageContext(**image_context)
        
        return request

    def annotate_image(
        self,
        image_path: Optional[str] = None,
        image_content: Optional[bytes] = None,
        features: Optional[list] = None,
        image_context: Optional[Dict[str, Any]] = None
    ) -> vision_v1.AnnotateImageResponse:
        """Execute annotation request against Google Cloud Vision API."""
        if image_path and image_content is None:
            image_content = self.encode_image_to_base64(image_path)
        
        if features is None:
            features = [self.create_feature("DOCUMENT_TEXT_DETECTION")]
        
        request = self.build_annotation_request(image_content, features, image_context)
        response = self.client.batch_annotate_images(requests=[request])
        return response.responses[0]

    def batch_annotate(self, requests: list) -> list:
        """Execute multiple annotation requests against Google Cloud Vision API."""
        response = self.client.batch_annotate_images(requests=requests)
        return response.responses


def get_vision_client() -> GoogleVisionClient:
    """Factory function to get a configured Google Vision API client."""
    return GoogleVisionClient()
