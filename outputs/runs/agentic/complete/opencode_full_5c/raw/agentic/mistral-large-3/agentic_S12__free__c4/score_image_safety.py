import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from typing import Dict, List, Optional


class ImageSafetyScorer:
    """Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision API."""

    def __init__(self):
        self.client = vision_v1.ImageAnnotatorClient()
        self.model = (
            "builtin/latest"  # Google Cloud Vision's safe search detection model
        )

    def score_safety(
        self, image_path: Optional[str] = None, image_content: Optional[bytes] = None
    ) -> Dict[str, str]:
        """Checks an image for unsafe or policy-sensitive visual content.

        Args:
            image_path: Local path to the image file.
            image_content: Raw image bytes.

        Returns:
            Dictionary containing safety ratings for adult, spoof, medical, violence, and racy content.
        """
        if image_path:
            with open(image_path, "rb") as image_file:
                content = image_file.read()
        elif image_content:
            content = image_content
        else:
            raise ValueError("Either image_path or image_content must be provided.")

        image = types.Image(content=content)
        response = self.client.safe_search_detection(image=image)
        safe_search = response.safe_search_annotation

        safety_ratings = {
            "adult": safe_search.adult.name,
            "spoof": safe_search.spoof.name,
            "medical": safe_search.medical.name,
            "violence": safe_search.violence.name,
            "racy": safe_search.racy.name,
        }

        return safety_ratings
