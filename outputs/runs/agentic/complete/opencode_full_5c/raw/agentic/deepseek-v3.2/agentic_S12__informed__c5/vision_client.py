import os
from google.cloud import vision
from typing import Optional, Dict, Any


class VisionClient:
    """Local configuration and client helper utilities for Static Image and Visual Understanding."""

    def __init__(self, credentials_path: Optional[str] = None):
        """Initialize Google Cloud Vision client.

        Args:
            credentials_path: Path to Google Cloud credentials JSON file.
                If None, uses GOOGLE_APPLICATION_CREDENTIALS environment variable.
        """
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        self.client = vision.ImageAnnotatorClient()

    def load_image(self, image_path: str) -> vision.Image:
        """Load image from file path."""
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        return vision.Image(content=content)

    def get_client(self) -> vision.ImageAnnotatorClient:
        """Get the Google Cloud Vision client instance."""
        return self.client

    @staticmethod
    def normalize_labels_response(labels) -> list:
        """Normalize label detection response."""
        return [
            {"description": label.description, "score": label.score, "mid": label.mid}
            for label in labels
        ]

    @staticmethod
    def normalize_text_response(texts) -> Dict[str, Any]:
        """Normalize text detection response."""
        if not texts:
            return {"full_text": "", "text_blocks": []}

        full_text = texts[0].description
        detected_texts = []

        for text in texts[1:]:
            detected_texts.append(
                {
                    "text": text.description,
                    "bounds": [
                        (vertex.x, vertex.y) for vertex in text.bounding_poly.vertices
                    ],
                }
            )

        return {"full_text": full_text, "text_blocks": detected_texts}

    @staticmethod
    def normalize_safety_response(safe_search) -> Dict[str, Any]:
        """Normalize safe search detection response."""
        safety_scores = {
            "adult": safe_search.adult.name,
            "spoof": safe_search.spoof.name,
            "medical": safe_search.medical.name,
            "violence": safe_search.violence.name,
            "racy": safe_search.racy.name,
        }

        is_safe = all(
            [
                safe_search.adult <= vision.Likelihood.POSSIBLE,
                safe_search.violence <= vision.Likelihood.POSSIBLE,
                safe_search.racy <= vision.Likelihood.POSSIBLE,
            ]
        )

        return {
            "safety_scores": safety_scores,
            "is_safe": is_safe,
            "overall_risk": "HIGH" if not is_safe else "LOW",
        }
