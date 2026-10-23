from typing import Dict, List, Optional
from vision_client import VisionClient
from vision_models import ImageLabel, ImageText, ImageSafety, ImageDescription


class ImageSummary:
    """Summarizes visual analysis results from Google Cloud Vision API."""

    def __init__(self):
        self.client = VisionClient()

    def summarize(
        self, image_path: Optional[str] = None, image_content: Optional[bytes] = None
    ) -> Dict[str, Any]:
        """Summarizes visual analysis results for an image.

        Args:
            image_path: Local path to the image file.
            image_content: Raw image bytes.

        Returns:
            Dictionary containing summarized visual analysis results.
        """
        image = self.client.load_image(image_path, image_content)

        # Detect multiple features in a single request
        feature_types = [
            vision_v1.Feature.Type.LABEL_DETECTION,
            vision_v1.Feature.Type.TEXT_DETECTION,
            vision_v1.Feature.Type.IMAGE_PROPERTIES,
            vision_v1.Feature.Type.SAFE_SEARCH_DETECTION,
        ]

        results = self.client.detect_features(image, feature_types)

        # Normalize results
        summary = {
            "labels": VisionModels.normalize_labels(results.get("labels", []))
            if results.get("labels")
            else [],
            "text": VisionModels.normalize_text(results.get("text", [])[1:])
            if results.get("text")
            else [],
            "safety": VisionModels.normalize_safety(results.get("safety", {}))
            if results.get("safety")
            else None,
            "colors": results.get("colors", []),
            "description": self._generate_description(results),
        }

        return summary

    def _generate_description(self, results: Dict[str, Any]) -> str:
        """Generates a human-readable description from analysis results."""
        description_parts = []

        if results.get("labels"):
            labels = [label.description for label in results["labels"]]
            description_parts.append(f"Likely contains: {', '.join(labels[:3])}.")

        if results.get("colors"):
            description_parts.append(
                f"Dominant colors: {', '.join(results['colors'][:3])}."
            )

        if results.get("text"):
            description_parts.append("Contains visible text.")

        return (
            " ".join(description_parts)
            if description_parts
            else "No description available."
        )
