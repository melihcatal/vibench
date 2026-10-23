import os
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from typing import Optional, Dict, Any


class VisionClient:
    """Local configuration and client helper utilities for Google Cloud Vision API."""

    def __init__(self):
        self.client = vision_v1.ImageAnnotatorClient()
        self._validate_credentials()

    def _validate_credentials(self) -> None:
        """Validates that Google Cloud credentials are available."""
        if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            raise EnvironmentError(
                "Google Cloud credentials not found. "
                "Set the GOOGLE_APPLICATION_CREDENTIALS environment variable."
            )

    def load_image(
        self, image_path: Optional[str] = None, image_content: Optional[bytes] = None
    ) -> types.Image:
        """Loads an image from a file path or raw bytes.

        Args:
            image_path: Local path to the image file.
            image_content: Raw image bytes.

        Returns:
            Google Cloud Vision Image object.
        """
        if image_path:
            with open(image_path, "rb") as image_file:
                content = image_file.read()
        elif image_content:
            content = image_content
        else:
            raise ValueError("Either image_path or image_content must be provided.")

        return types.Image(content=content)

    def detect_features(
        self, image: types.Image, feature_types: List[types.Feature.Type]
    ) -> Dict[str, Any]:
        """Detects multiple features in an image.

        Args:
            image: Google Cloud Vision Image object.
            feature_types: List of feature types to detect.

        Returns:
            Dictionary containing detection results for each feature type.
        """
        features = [types.Feature(type_=feature_type) for feature_type in feature_types]
        request = types.AnnotateImageRequest(image=image, features=features)
        response = self.client.annotate_image(request)

        results = {}
        if response.label_annotations:
            results["labels"] = [
                label.description for label in response.label_annotations
            ]
        if response.text_annotations:
            results["text"] = [text.description for text in response.text_annotations]
        if response.image_properties_annotation:
            results["colors"] = [
                f"{color.color.red}, {color.color.green}, {color.color.blue}"
                for color in response.image_properties_annotation.dominant_colors.colors
            ]
        if response.safe_search_annotation:
            results["safety"] = {
                "adult": response.safe_search_annotation.adult.name,
                "spoof": response.safe_search_annotation.spoof.name,
                "medical": response.safe_search_annotation.medical.name,
                "violence": response.safe_search_annotation.violence.name,
                "racy": response.safe_search_annotation.racy.name,
            }

        return results
