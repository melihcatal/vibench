import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from typing import List, Optional


class ImageTextDetector:
    """Detects text appearing inside an image using Google Cloud Vision API."""

    def __init__(self):
        self.client = vision_v1.ImageAnnotatorClient()
        self.model = "builtin/latest"  # Google Cloud Vision's text detection model

    def detect_text(
        self, image_path: Optional[str] = None, image_content: Optional[bytes] = None
    ) -> List[str]:
        """Detects text in an image.

        Args:
            image_path: Local path to the image file.
            image_content: Raw image bytes.

        Returns:
            List of detected text snippets.
        """
        if image_path:
            with open(image_path, "rb") as image_file:
                content = image_file.read()
        elif image_content:
            content = image_content
        else:
            raise ValueError("Either image_path or image_content must be provided.")

        image = types.Image(content=content)
        response = self.client.text_detection(image=image)
        texts = [text.description for text in response.text_annotations]

        return texts
