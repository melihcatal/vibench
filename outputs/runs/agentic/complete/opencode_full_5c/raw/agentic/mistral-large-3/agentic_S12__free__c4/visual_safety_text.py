from typing import List, Dict, Optional
from google.cloud import language_v1
from vision_client import VisionClient
from vision_models import ImageLabel


class VisualSafetyTextChecker:
    """Checks generated visual labels for unsafe text using Google Cloud Natural Language API."""

    def __init__(self):
        self.vision_client = VisionClient()
        self.language_client = language_v1.LanguageServiceClient()
        self.model = "text-models/v1"  # Google Cloud Natural Language API model

    def check_labels_for_unsafe_text(
        self, image_path: Optional[str] = None, image_content: Optional[bytes] = None
    ) -> Dict[str, Any]:
        """Checks visual labels for unsafe or sensitive content.

        Args:
            image_path: Local path to the image file.
            image_content: Raw image bytes.

        Returns:
            Dictionary containing unsafe label analysis results.
        """
        image = self.vision_client.load_image(image_path, image_content)

        # Detect labels
        feature_types = [vision_v1.Feature.Type.LABEL_DETECTION]
        results = self.vision_client.detect_features(image, feature_types)

        labels = results.get("labels", [])
        unsafe_labels = self._analyze_labels_for_safety(labels)

        return {"labels": labels, "unsafe_labels": unsafe_labels}

    def _analyze_labels_for_safety(
        self, labels: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Analyzes labels for unsafe or sensitive content."""
        unsafe_labels = []

        for label in labels:
            document = language_v1.Document(
                content=label.description, type_=language_v1.Document.Type.PLAIN_TEXT
            )

            response = self.language_client.analyze_sentiment(
                request={"document": document}
            )

            # Check for negative sentiment or sensitive content
            if response.document_sentiment.score < -0.5:
                unsafe_labels.append(
                    {
                        "label": label.description,
                        "score": label.score,
                        "sentiment_score": response.document_sentiment.score,
                        "sentiment_magnitude": response.document_sentiment.magnitude,
                    }
                )

        return unsafe_labels
