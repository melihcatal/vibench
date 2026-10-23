# [HELPER] document_client.py

import os
from typing import Optional
from google.cloud import vision_v1

# Provider-specific environment variable for credentials handling
VISION_PROJECT = os.getenv("VISION_PROJECT_ID")

class VisionClient:
    def __init__(self):
        # Initialize Google Cloud Vision client with default credentials (supports env vars like GOOGLE_APPLICATION_CREDENTIALS)
        self.service = vision_v1.ImageAnnotatorClient()
        # Optionally set project explicitly
        if VISION_PROJECT:
            self.service._session_kwargs["client_options"] = {"api_endpoint": f"vision.googleapis.com"}
        # In production you would configure custom retry, timeout, etc.

    def extract_text(self, image_bytes: bytes) -> str:
        """Convenient wrapper to return raw full text from OCR."""
        image = vision_v1.types.Image(content=image_bytes)
        response = self.service.document_text_detection(image=image)
        return response.full_text_annotation.text
